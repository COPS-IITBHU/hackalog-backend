from rest_framework import serializers, exceptions
from django.utils import timezone
from django.utils.crypto import get_random_string
from .models import Hackathon, Team, Submission
from authentication.models import User

class TeamSerializer(serializers.ModelSerializer):
    hackathon = serializers.SerializerMethodField()

    def get_hackathon(self,obj):
        serializer = HackathonSerializer(obj.hackathon)
        return serializer.data

    class Meta:
        model = Team
        fields = ('id', 'name', 'hackathon', 'team_id')
        depth = 1

class TeamCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        name = attrs['name']
        hackathon_slug = self.context['kwargs']['slug']
        user = self.context['request'].user
        try:
            hackathon = Hackathon.objects.get(slug=hackathon_slug)
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound(detail="Hackathon does not exist!")
        try:
            team = Team.objects.get(hackathon=hackathon, members=user)
        except:
            pass
        else:
            raise exceptions.ValidationError(detail="You are already part of a team in this hackathon.")
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
        hackathon_slug = self.context['kwargs']['slug']
        hackathon = Hackathon.objects.get(slug=hackathon_slug)
        team = Team.objects.create(name=data['name'], hackathon=hackathon, leader=leader, team_id=get_random_string(16))
        team.members.set(members)
        team.save()
        return team
    class Meta:
        model = Team
        fields = ('name',)

class JoinTeamSerializer(serializers.Serializer):

    def join_team(self):
        hackathon_slug = self.context['kwargs']['slug']
        team_id = self.context['kwargs']['team_id']
        try:
            hackathon = Hackathon.objects.get(slug=hackathon_slug)
            team = Team.objects.get(team_id=team_id, hackathon=hackathon)
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound(detail="Hackathon does not exist!")
        except Team.DoesNotExist:
            raise exceptions.NotFound(detail="Team does not exist!")
        user = self.context['request'].user
        team_qs = Team.objects.filter(hackathon=hackathon, members= user)
        if team_qs.exists():
            print('team_qs =', team_qs)
            raise exceptions.ValidationError(detail="You are already part of some team in this hackathon.")
        else:
            members = team.members
            if user in members.all():
                raise exceptions.ValidationError(detail="You are already in the team!")
            members.add(user)

class HackathonSerializer(serializers.ModelSerializer):
    status = serializers.CharField()

    def validate_end(self, end):
        if end < timezone.now():
            raise serializers.ValidationError('End date cannot be in past')
        return end

    def validate_start(self, start):
        if start < timezone.now():
            raise serializers.ValidationError('Start date cannot be in past')
        return start

    def validate(self, attrs):
        if attrs['start'] > attrs['end']:
            raise serializers.ValidationError('Event ends before starting')
        return attrs

    class Meta:
        model = Hackathon
        fields = '__all__'

class HackathonDetailSerializer(HackathonSerializer):
    userStatus = serializers.SerializerMethodField('get_userStatus')

    def get_userStatus(self, obj):
        '''
        Serializer Field to show about the status of the hackathon
        with respect to the current user
        '''
        request = self.context['request']
        if not request.auth:
            return False
        teams = Team.objects.filter(members=request.user, hackathon=obj)
        submissions = []
        for team in teams:
            submissions.extend(
                Submission.objects.filter(hackathon=obj, team=team)
            )
        if not teams.count():
            return 'not registered'
        elif not len(submissions):
            return 'registered'
        return 'submitted'


class SubmissionsSerializer(serializers.ModelSerializer):
    teamName = serializers.SerializerMethodField('get_teamName')
    
    def get_teamName(self, obj):
        '''
        Serializer Field to show team name 
        without the need of full team details
        '''
        try:
            team = Team.objects.get(pk = obj.team_id)
        except Team.DoesNotExist:
            raise exceptions.ValidationError(detail='Team does not exists.') 
        return team.name

    class Meta:
        model = Submission
        fields = '__all__'

    def validate_score(self, score):
        if score < 0:
            raise serializers.ValidationError("Score can't be less than 0")
        return score
        
class MemberExitSerializer(serializers.Serializer):

    def exit_team(self):
        team_id = self.context['kwargs']['team_id']
        try:
            team = Team.objects.get(team_id=team_id)
        except Team.DoesNotExist:
            raise exceptions.ValidationError(detail='Team does not exists.')
        user = self.context['request'].user  # requesting user
        username = self.context['kwargs']['username'] # username to be removed from team
        if (team.leader.username != username) and (user == team.leader or user.username == username):
            hackathon = team.hackathon
            if hackathon.start < timezone.now():
                raise exceptions.ValidationError(detail='Cannot leave/exit team as event started.')
            try:
                member = User.objects.get(username=username)
            except User.DoesNotExist:
                raise exceptions.NotFound(detail='No user with given username')
            members = team.members
            if member not in members.all():
                raise exceptions.ValidationError(detail='Already not in team')
            members.remove(member)
            team.save()
        else:
            raise exceptions.PermissionDenied('You are not allowed to perform this operation.')

class SubmissionRUDSerializer(serializers.ModelSerializer): 
    hackathon = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    def get_hackathon(self,obj):
        serializer = HackathonSerializer(obj.hackathon)
        return serializer.data

    def get_team(self, obj):
        serializer = TeamSerializer(obj.team)
        return serializer.data

    class Meta:
        model = Submission
        fields = ('title', 'team', 'review', 'hackathon', 'submission_url', 'score', 'description')
        read_only_fields = ['score']
