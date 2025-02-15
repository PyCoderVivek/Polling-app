from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, PollOption, Vote
from .forms import PollForm, VoteForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from Authentication.models import User
from django.db.models.functions import TruncDate
from django.http import HttpResponseForbidden



def poll_visualizations_view(request):
    polls = Poll.objects.all()
    poll_data = []

    for poll in polls:
        options = poll.options.all()
        labels = [option.option_text for option in options]
        data = [option.votes.count() for option in options]

        poll_data.append({
            'poll': poll,
            'labels': labels,
            'data': data,
        })

    return render(request, 'polls/poll_visualizations.html', {
        'poll_data': poll_data,
    })

@login_required
def create_poll_view(request):
    if request.method == "POST":
        poll_form = PollForm(request.POST, request.FILES)  # Include request.FILES to handle file upload
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.creator = request.user  # Associate poll with the user
            poll.save()
            options = request.POST.getlist('options')  # Get options from the form
            for option_text in options:
                PollOption.objects.create(poll=poll, option_text=option_text)
            return redirect('poll_list')  # Redirect to the poll list after saving
    else:
        poll_form = PollForm()
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form})

@login_required
def delete_poll_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    # Only allow the creator or an admin to delete the poll
    if request.user == poll.creator or request.user.is_superuser:
        poll.delete()
        return redirect('poll_list')  # Redirect to the list of polls after deletion
    else:
        return HttpResponseForbidden("You are not allowed to delete this poll.")

def vote_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    options = poll.options.all()
    
    user_has_voted = request.user.is_authenticated and Vote.objects.filter(poll=poll, user=request.user).exists()

    if user_has_voted:
        return redirect('poll_results', poll_id=poll.id)

    if request.method == 'POST':
        form = VoteForm(request.POST)
        form.fields['choice'].choices = [(o.id, o.option_text) for o in options]
        if form.is_valid():
            selected_option_id = form.cleaned_data['choice']
            selected_option = get_object_or_404(PollOption, id=selected_option_id)
            Vote.objects.create(poll=poll, option=selected_option, user=request.user if request.user.is_authenticated else None)
            return redirect('poll_results', poll_id=poll.id)
    else:
        form = VoteForm()
        form.fields['choice'].choices = [(o.id, o.option_text) for o in options]

    return render(request, 'polls/vote.html', {'poll': poll, 'form': form, 'user_has_voted': user_has_voted})

def poll_list_view(request):
    polls = Poll.objects.all()
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_results_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    options = poll.options.all()
    option_votes = {option: option.votes.count() for option in options}
    
    total_votes = sum(option_votes.values()) 

    option_percentages = {option: (votes / total_votes * 100) if total_votes > 0 else 0 for option, votes in option_votes.items()}

    labels = [option.option_text for option in options]
    data = [option_votes[option] for option in options]

    return render(request, 'polls/results.html', {
        'poll': poll,
        'option_votes': option_votes,
        'total_votes': total_votes,
        'option_percentages': option_percentages,  # Pass the calculated percentages
        'labels': labels,
        'data': data,
    })

@user_passes_test(lambda u: u.is_superuser)
def analytics_dashboard_view(request):
    # Total number of polls
    total_polls = Poll.objects.count()

    # Total number of votes
    total_votes = Vote.objects.count()

    # Top 5 polls with the most votes
    top_polls = Poll.objects.annotate(vote_count=Count('votes')).order_by('-vote_count')[:5]

    # Top 5 users who have cast the most votes
    top_voters = User.objects.annotate(vote_count=Count('vote')).order_by('-vote_count')[:5]

    context = {
        'total_polls': total_polls,
        'total_votes': total_votes,
        'top_polls': top_polls,
        'top_voters': top_voters,
    }

    return render(request, 'polls/analytics_dashboard.html', context)

def poll_search(request):
    query = request.GET.get('query')
    polls = Poll.objects.filter(title__icontains=query) | Poll.objects.filter(question__icontains=query)
    return render(request, 'polls/poll_list.html', {'polls': polls})

@login_required
def user_dashboard_view(request):
    user = request.user
    polls = Poll.objects.filter(creator=user)
    
    # Total Polls and Votes
    total_polls = polls.count()
    total_votes = Vote.objects.filter(poll__creator=user).count()

    poll_data = []
    for poll in polls:
        options = poll.options.all()
        labels = [option.option_text for option in options]
        data = [option.votes.count() for option in options]
        total_votes_for_poll = sum(data)  # Sum votes for this poll
        vote_percentage = (total_votes_for_poll / total_votes * 100) if total_votes > 0 else 0

        poll_data.append({
            'poll': poll,
            'options': options,
            'labels': labels,
            'data': data,
            'total_votes': total_votes_for_poll,
            'vote_percentage': vote_percentage,
        })

    # Votes over time
    votes_over_time = (Vote.objects
                        .filter(poll__creator=user)
                        .annotate(date=TruncDate('timestamp'))  # Assuming you have a 'timestamp' field in Vote model
                        .values('date')
                        .annotate(vote_count=Count('id'))
                        .order_by('date'))

    vote_time_labels = [v['date'].strftime('%Y-%m-%d') for v in votes_over_time]
    vote_time_data = [v['vote_count'] for v in votes_over_time]

    context = {
        'poll_data': poll_data,
        'total_polls': total_polls,
        'total_votes': total_votes,
        'vote_time_labels': vote_time_labels,
        'vote_time_data': vote_time_data,
    }

    return render(request, 'polls/user_dashboard.html', context)