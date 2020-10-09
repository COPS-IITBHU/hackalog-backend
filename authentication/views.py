from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from .models import UserProfile, User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (LoginSerializer, ResponseSerializer)

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
        user = serializer.validated_data['user']
        token = create_auth_token(user)
        response = ResponseSerializer({'token':token})
        return Response(response.data,status.HTTP_200_OK)