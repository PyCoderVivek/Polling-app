#Authenticate/forms.py


from django import forms
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class CustomLoginForm(AuthenticationForm):
    is_admin = forms.BooleanField(required=False, label='Log in as Admin')