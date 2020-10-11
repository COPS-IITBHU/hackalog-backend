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
            raise serializers.ValidationError("Invalid Firebase Token")

    def validate(self, data):
        id_token = data.get('id_token', None)
        user = None
        jwt = self.validate_access_token(id_token)
        uid = jwt['uid']
        profile = UserProfile.objects.filter(uid=uid)

        if profile:
            user = profile[0].user
        else:
            email = jwt['email']
            user = User()
            user.username = jwt['uid']
            user.email = email
            user.save()
            profile = UserProfile.objects.create(
                user=user, email=email)

        data['user'] = user
        return data

class ProfileSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        name = validated_data['name']
        college = validated_data['college']
        github_handle = validated_data['github_handle']
        bio = validated_data['bio']
        interests = validated_data['interests']
        instance.name = name
        instance.college = college
        instance.github_handle = github_handle
        instance.bio = bio
        instance.interests = interests
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        read_only_fields = ('uid', 'email')
        fields = ('uid', 'name', 'email', 'college', 'github_handle', 'bio', 'interests')
