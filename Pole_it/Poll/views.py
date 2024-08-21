#  Poll/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, PollOption, Vote
from .forms import PollForm, VoteForm
from django.contrib import messages
from .models import Poll, PollOption
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test



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


def create_poll_view(request):
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save()
            options = request.POST.getlist('options')
            for option_text in options:
                PollOption.objects.create(poll=poll, option_text=option_text)
            return redirect('poll_list')  # Redirect to a page that lists all polls
    else:
        poll_form = PollForm()
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form})

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
    
    # Prepare data for Chart.js
    labels = [option.option_text for option in options]
    data = [option.votes.count() for option in options]

    return render(request, 'polls/results.html', {
        'poll': poll, 
        'option_votes': option_votes,
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