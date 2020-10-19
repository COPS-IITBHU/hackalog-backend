from django.urls import path
from .views import HackathonTeamListView, HackathonTeamCreateView, HackathonListView, HackathonsRUDView, HackathonCreateView

urlpatterns = [
    path('hackathons/<int:pk>/teams/', HackathonTeamListView.as_view()),
    path('hackathons/add-team/', HackathonTeamCreateView.as_view()),
    path('hackathons/list/', HackathonListView.as_view()),
    path('hackathons/', HackathonCreateView.as_view(), name='Hackathon Create View'),
    path('hackathons/<int:pk>', HackathonsRUDView.as_view(), name='Hackathon Read, Edit and Delete View'),
]
