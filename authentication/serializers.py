from rest_framework import serializers
from .utils import FirebaseAPI
from .models import User
from rest_framework.exceptions import ParseError
from drf_yasg.utils import swagger_serializer_method
from django.conf import settings
from django.contrib.auth import get_user_model

class ResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)

class LoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(max_length=2400)

    def validate_access_token(self, access_token):
        return FirebaseAPI.verify_id_token(access_token)

    def validate(self, data):
        User = get_user_model()
        id_token = data.get('id_token', None)
        current_user = None
        jwt = self.validate_access_token(id_token)
        username = jwt['uid']
        profile = User.objects.filter(username=username)

        if profile:
            current_user = profile[0]
        else:
            email = jwt['email']
            name = jwt['name']
            profile = User.objects.create(name = name, username = username, email = email)

        data['profile'] = current_user
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        read_only_fields = (
            'id', 'email', 'username')
        fields = ('username', 'name','handle', 'college', 'github_handle', 'bio', 'interests')