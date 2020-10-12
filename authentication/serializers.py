from rest_framework import serializers
from .utils import FirebaseAPI
from .models import User, UserProfile
from rest_framework.exceptions import ParseError
from drf_yasg.utils import swagger_serializer_method

class ResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)

class LoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(max_length=2400)

    def validate_access_token(self, access_token):
        return FirebaseAPI.verify_id_token(access_token)

    def validate(self, data):
        id_token = data.get('id_token', None)
        current_user = None
        jwt = self.validate_access_token(id_token)
        uid = jwt['uid']
        profile = UserProfile.objects.filter(uid=uid)

        if profile:
            current_user = profile[0].user
        else:
            email = jwt['email']
            name = jwt['name']
            user = User()
            user.email = email
            user.username = jwt['uid']
            user.save()
            current_user = user
            profile = UserProfile.objects.create(
                uid=uid, user=user, name=name, email=email)

        data['user'] = current_user
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('uid', 'name','handle', 'college', 'github_handle', 'bio', 'interests')
