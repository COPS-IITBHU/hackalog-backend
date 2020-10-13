from django.urls import path
from .views import LoginView, ProfileView, ProfileRetrieveView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:handle>', ProfileRetrieveView.as_view(), name='get_profile'),
]