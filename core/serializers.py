from rest_framework import serializers, exceptions
from authentication.models import User
from django.utils.crypto import get_random_string
from .models import Hackathon, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        exclude = ['leader', 'members']
        depth = 1

class TeamCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        name = attrs['name']
        hackathon_id = self.context['kwargs']['pk']
        try:
            hackathon = Hackathon.objects.get(id=hackathon_id)
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound(detail="Hackathon does not exist!")
        try:
            team = Team.objects.get(hackathon=hackathon, name=name)
        except:
            pass
        else:
            raise exceptions.ValidationError(detail="Team with this name already exists in the Hackathon!")
        return attrs

    def save(self):
        data = self.validated_data
        user = self.context['request'].user
        leader = user
        members = [user]
        hackathon_id = self.context['kwargs']['pk']
        hackathon = Hackathon.objects.get(id=hackathon_id)
        team = Team.objects.create(name=data['name'], hackathon=hackathon, leader=leader, team_id=get_random_string(16))
        team.members.set(members)
        team.save()
        return team
    class Meta:
        model = Team
        fields = ('name',)

class JoinTeamSerializer(serializers.Serializer):

    def join_team(self):
        hackathon_id = self.context['kwargs']['pk']
        team_id = self.context['kwargs']['team_id']
        try:
            hackathon = Hackathon.objects.get(id=hackathon_id)
            team = Team.objects.get(team_id=team_id, hackathon=hackathon)
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound(detail="Hackathon does not exist!")
        except Team.DoesNotExist:
            raise exceptions.NotFound(detail="Team does not exist!")
        user = self.context['request'].user
        members = team.members
        if user in members.all():
            raise exceptions.ValidationError(detail="You are already in the team!")
        members.add(user)

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = '__all__'
