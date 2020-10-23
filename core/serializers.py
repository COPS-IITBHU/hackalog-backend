from rest_framework import serializers
from authentication.models import User

from .models import Hackathon, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class TeamCreateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        hackathon_id = self.context.get('view').kwargs['pk']
        if hackathon_id != data['hackathon']:
            raise serializers.ValidationError("Mismatch of Hackathon ID in url and request body!")
        return data
    class Meta:
        model = Team
        fields = '__all__'

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'
