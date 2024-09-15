#Authenticate/forms.py


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

class CustomLoginForm(AuthenticationForm):
    is_admin = forms.BooleanField(required=False, label='Log in as Admin')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'location']