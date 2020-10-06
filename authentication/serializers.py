from rest_framework import serializers
from .utils import Profile, FirebaseAPI
from .models import User, UserProfile
from rest_framework.exceptions import ParseError
from drf_yasg.utils import swagger_serializer_method

class ResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)

class RegisterSerializer(serializers.Serializer):
    id_token=serializers.CharField(max_length=2400)

    def validate_id_token(self, access_token):
        return FirebaseAPI.verify_id_token(access_token)

    def validate(self, data):
        jwt = data['id_token']
        email = FirebaseAPI.get_email(jwt)
        if Profile.verify_email(email):
            pass
        else:
            raise serializers.ValidationError("Please try again")

    def get_user(self, jwt):
        user = User()
        user.username = jwt['uid']
        user.last_name = FirebaseAPI.get_name(jwt)
        user.email = FirebaseAPI.get_email(jwt)
        return user

    def create(self, validated_data):
        data = validated_data
        jwt = data['id_token']
        uid = jwt['uid']
        user = self.get_user(jwt)
        try:
            user.validate_unique()
        # pylint: disable=no-member
        except Exception as e:
            raise serializers.ValidationError("Already Registered. Please login.")
        user.save()
        # pylint: disable=no-member
        profile = UserProfile.objects.get_or_create(
            pk=uid, user=user, name=user.last_name, email=user.email
        )
        return user

class LoginSerializer(serializers.Serializer):
    id_token = serializers.CharField(max_length=2400)

    def validate_access_token(self, access_token):
        return FirebaseAPI.verify_id_token(access_token)

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
            if not Profile.verify_email(email):
                raise serializers.ValidationError(
                    "Please try again")
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