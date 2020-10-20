from django.urls import path
from .views import  HackathonListView, HackathonsRUDView, HackathonCreateView, HackathonTeamView

urlpatterns = [
    path('hackathons/<int:pk>/teams/', HackathonTeamView.as_view()),
    path('hackathons/list/', HackathonListView.as_view()),
    path('hackathons/', HackathonCreateView.as_view(), name='Hackathon Create View'),
    path('hackathons/<int:pk>', HackathonsRUDView.as_view(), name='Hackathon Read, Edit and Delete View'),
]
