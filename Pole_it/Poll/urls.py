# Poll/urls.py

from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', create_poll_view, name='create_poll'),
    path('vote/<int:poll_id>/', vote_view, name='vote'),
    path('', poll_list_view, name='poll_list'),
    path('results/', poll_visualizations_view, name='poll_visualizations'), 
    path('results/<int:poll_id>/', poll_results_view, name='poll_results'),
    path('analytics/', analytics_dashboard_view, name='analytics_dashboard'),  # New URL for the dashboard
    path('polls/search/', poll_search, name='poll_search'),  # Add this line

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
