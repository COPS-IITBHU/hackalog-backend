from django.urls import path
from .views import HackathonTeamListView, HackathonTeamCreateView, HackathonListView

urlpatterns = [
    path('hackathons/<int:id>/teams/', HackathonTeamListView.as_view()),
    path('hackathons/add-team/', HackathonTeamCreateView.as_view()),
    path('hackathons/list/', HackathonListView.as_view())
]