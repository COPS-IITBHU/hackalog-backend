from rest_framework import serializers
from .utils import FirebaseAPI
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
        uid = jwt['uid']
        profile = User.objects.filter(uid=uid)

        if profile:
            current_user = profile[0]
        else:
            email = FirebaseAPI.get_email(jwt)
            name = FirebaseAPI.get_name(jwt)
            profile = User.objects.create(uid = uid,name = name, email = email)
            current_user = profile

        data['profile'] = current_user
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('name','username', 'college', 'github_handle', 'bio', 'interests')