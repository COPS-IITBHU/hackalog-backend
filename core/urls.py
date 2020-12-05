from django.urls import path
from .views import  HackathonsRUDView, HackathonListCreateView, HackathonTeamView, JoinTeamView, HackathonSubmissionView, TeamView, MemberExitView

urlpatterns = [
    path('hackathons/<int:pk>/teams/', HackathonTeamView.as_view()),
    path('hackathons/', HackathonListCreateView.as_view(), name='Hackathon List/Create View'),
    path('hackathons/<int:pk>/', HackathonsRUDView.as_view(), name='Hackathon Read, Edit and Delete View'),
    path('hackathons/<int:pk>/teams/join/<str:team_id>/', JoinTeamView.as_view()),
    path('hackathons/<int:pk>/submissions/', HackathonSubmissionView.as_view()),
    path('teams/<str:team_id>/', TeamView.as_view(), name='Team Read, Edit, Delete View'),
    path('teams/<str:team_id>/member-exit/<str:username>', MemberExitView.as_view())
]
