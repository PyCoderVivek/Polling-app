#Authenticate/forms.py


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    is_admin = forms.BooleanField(required=False, label='Log in as Admin')