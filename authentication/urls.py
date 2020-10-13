from django.urls import path
from .views import LoginView, ProfileView, UserDetail

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>', UserDetail.as_view(), name='get_profile'),
]