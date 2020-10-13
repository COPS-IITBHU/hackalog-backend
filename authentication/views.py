from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from .models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import (
    LoginSerializer, ResponseSerializer, ProfileSerializer)

def create_auth_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token

class LoginView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.validated_data['profile']
        token = create_auth_token(profile)
        response = ResponseSerializer({'token':token})
        return Response(response.data,status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        User = get_user_model()
        return User.objects.get(uid = self.request.user.uid)

class UserDetail(generics.RetrieveAPIView):
    User = get_user_model()
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = ProfileSerializer