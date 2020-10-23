from django.urls import path
from .views import  HackathonsRUDView, HackathonListCreateView, HackathonTeamView

urlpatterns = [
    path('hackathons/<int:pk>/teams/', HackathonTeamView.as_view()),
    path('hackathons/', HackathonListCreateView.as_view(), name='Hackathon List/Create View'),
    path('hackathons/<int:pk>/', HackathonsRUDView.as_view(), name='Hackathon Read, Edit and Delete View'),
]
