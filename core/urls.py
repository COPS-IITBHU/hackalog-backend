from django.urls import path
from .views import (HackathonsRUDView,HackathonCreateView)

urlpatterns = [   
    path('hackathons/', HackathonCreateView.as_view(), name='Hackathon Create View'),
    path('hackathons/<int:id>', HackathonsRUDView.as_view(), name='Hackathon Read, Edit and Delete View'),
]
