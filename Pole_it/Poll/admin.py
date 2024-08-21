# Poll/admin.py

from django.contrib import admin
from .models import Poll, PollOption, Vote

# Register your models here.
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(Vote)
