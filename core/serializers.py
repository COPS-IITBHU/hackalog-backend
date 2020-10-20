from rest_framework import serializers
from authentication.models import User

from .models import Hackathon, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'

class HackathonTeamCreateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if(data['leader'] not in data['members']):
            raise serializers.ValidationError("Leader of the team is not in Members list.")
        if(self.context['request'].user not in data['members']):
            raise serializers.ValidationError("Cannot create a team without including yourself.")

        return data

    class Meta:
        model = Team
        fields = '__all__'
