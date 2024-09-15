# Authentication/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Poll.models import Poll
from .models import UserProfile
from .forms import CustomLoginForm
from .forms import UserProfileForm
from .models import UserProfile

def landing_page(request):
    return render(request, 'auth/landingPage.html')

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
                # Automatically create UserProfile if it doesn't exist
                if not UserProfile.objects.filter(user=user).exists():
                    UserProfile.objects.create(user=user)

                # Admin-specific login
                if is_admin and user.is_superuser:
                    login(request, user)
                    return redirect('analytics_dashboard')  # Redirect to admin dashboard
                elif not is_admin:
                    login(request, user)
                    return redirect('home')  # Redirect to the home page or user dashboard
        else:
            messages.error(request, "Username or Password is invalid!")  # Handle invalid form submission
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
            UserProfile.objects.create(user=user)  # Create UserProfile instance during signup
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            return render(request, 'auth/signup.html')

    return render(request, 'auth/signup.html')

@login_required
def view_profile(request):
    """ View profile details """
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'auth/view_profile.html', context)

@login_required
def edit_profile(request):
    """ Update profile details """
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {'form': form}
    return render(request, 'auth/edit_profile.html', context)