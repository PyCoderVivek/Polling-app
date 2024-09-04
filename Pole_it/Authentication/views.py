# Athenticate/views.py

from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Poll.models import Poll
from .forms import UserProfileForm
from .models import UserProfile
from .forms import CustomLoginForm


@login_required
def view_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile does not exist.")
        return redirect('edit_profile')  # Redirect to profile creation/edit page

    return render(request, 'auth/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'auth/edit_profile.html', {'form': form})


@login_required
def home_view(request):
    user = request.user
    polls = Poll.objects.all()
    poll_results = []

    for poll in polls:
        options = poll.options.all()
        labels = [option.option_text for option in options]
        data = [option.votes.count() for option in options]

        poll_results.append({
            'poll': poll,
            'labels': labels,
            'data': data,
        })

    context = {
        'user': user,
        'role': 'Superuser' if user.is_superuser else 'Regular User',
        'poll_results': poll_results
    }
    return render(request, 'HomePage.html', context)

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            is_admin = form.cleaned_data.get('is_admin')

            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_active:
                if is_admin and user.is_superuser:
                    login(request, user)
                    return redirect('analytics_dashboard')  # Redirect to the admin dashboard
                elif not is_admin:
                    login(request, user)
                    return redirect('home')  # Redirect to the home page or user dashboard
        else:
            messages.error(request, "UserName or Password is Invalid !")  # Handle invalid form submission
    else:
        form = CustomLoginForm()

    return render(request, 'auth/login.html', {'form': form})

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'auth/signup.html')

        if password == password_confirm:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)  # Create UserProfile instance
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            return render(request, 'auth/signup.html')

    return render(request, 'auth/signup.html')
