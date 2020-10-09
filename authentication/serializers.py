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
        try:
            return FirebaseAPI.verify_id_token(access_token)
        except:
            return serializers.ValidationError("Invalid Firebase Token")
            
    def validate(self, data):
        id_token = data.get('id_token', None)
        user = None
        jwt = self.validate_access_token(id_token)
        uid = jwt['uid']
        # pylint: disable=no-member
        profile = UserProfile.objects.filter(uid=uid)

        if profile:
            user = profile[0].user
        else:
            email = jwt['email']
            name = jwt['name']
            user = User()
            user.username = jwt['uid']
            user.email = email
            user.save()
            user = user
            profile = UserProfile.objects.create(
                uid=uid, user=user, name=name, email=email)

        data['user'] = user
        return data