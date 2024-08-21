#Poll/forms.py

from django.db import models
from django.contrib.auth.models import User



class Poll(models.Model):
    title = models.CharField(max_length=200)
    question = models.TextField()

    def __str__(self):
        return self.title

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)

    def __str__(self):
        return self.option_text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('poll', 'user')  # Ensures a user can only vote once per poll

    def __str__(self):
        return f'{self.user} voted for {self.option} in {self.poll}'
