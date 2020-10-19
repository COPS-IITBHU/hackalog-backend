from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
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

@method_decorator(name='get', decorator=swagger_auto_schema(operation_id='user_profile_read'))
class UserDetail(generics.RetrieveAPIView):
    User = get_user_model()
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = ProfileSerializer