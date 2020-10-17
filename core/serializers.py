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

class HackathonTeamListSerializer(serializers.ModelSerializer):
    hackathon_teams = serializers.SerializerMethodField()

    def get_hackathon_teams(self, hackathon):
        teams = Team.objects.filter(hackathon=hackathon)
        serializer = TeamSerializer(teams, many=True)
        return serializer.data

    class Meta:
        model = Hackathon
        fields = ('hackathon_teams',)

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
