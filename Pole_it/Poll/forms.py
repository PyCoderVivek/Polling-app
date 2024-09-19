# Poll/forms.py

from django import forms
from .models import Poll

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'question']

class VoteForm(forms.Form):
    choice = forms.ChoiceField(widget=forms.RadioSelect)
