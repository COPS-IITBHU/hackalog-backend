from django.db import reset_queries
from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import get_list_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Hackathon, Team, Submission
from .serializers import HackathonSerializer, TeamSerializer, TeamCreateSerializer, JoinTeamSerializer, SubmissionsSerializer, MemberExitSerializer, SubmissionRUDSerializer,HackathonDetailSerializer
from .permissions import HackathonPermissions, AllowCompleteProfile, IsLeaderOrSuperUser
from authentication.serializers import ProfileSerializer


class HackathonTeamView(generics.ListCreateAPIView):
    """
    get:
    Returns a list of teams in a particular hackathon
    post:
    Creates a new team in a hackathon and return the team_id
    """
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated(), AllowCompleteProfile()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeamSerializer
        else:
            return TeamCreateSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'kwargs': self.kwargs
        }

    def get_queryset(self, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return None
        try:
            hackathon = Hackathon.objects.get(slug=self.kwargs['slug'])
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound("Hackathon does not exist!")
        queryset = Team.objects.filter(hackathon=hackathon)
        return queryset

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        data = {"team_id": team.team_id}
        return Response(data, status=status.HTTP_201_CREATED)


class JoinTeamView(generics.GenericAPIView):
    """
    patch:
    Join a team with team_id and hackathon_id
    """
    serializer_class = JoinTeamSerializer
    permission_classes = [permissions.IsAuthenticated, AllowCompleteProfile]
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        pass

    def get_serializer_context(self):
        return {
            'request': self.request,
            'kwargs': self.kwargs
        }

    def patch(self, request, **kwargs):
        serializer = self.get_serializer()
        serializer.join_team()
        return Response("Successfully jonied team!", status=status.HTTP_200_OK)


query_param = openapi.Parameter(
    'query', openapi.IN_QUERY, description="Query parameter - Returns all hackthons if not specified.",
    type=openapi.TYPE_STRING, enum=['completed', 'upcoming', 'ongoing'])


@method_decorator(name="get", decorator=swagger_auto_schema(manual_parameters=[query_param]))
class HackathonListCreateView(generics.ListCreateAPIView):
    """
    get:
    Returns list of Hackathons according to query parameter.

    post:
    Creates a new hackathon. Only admin can create a hackathon
    """
    serializer_class = HackathonSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = Hackathon.objects.all()
        query = self.request.query_params.get('query', None)
        current_date = timezone.now()
        if query is not None:
            if(query == 'ongoing'):
                queryset = Hackathon.objects.filter(
                    start__lt=current_date, end__gt=current_date)
            elif(query == 'completed'):
                queryset = Hackathon.objects.filter(
                    start__lt=current_date, end__lt=current_date)
            elif(query == 'upcoming'):
                queryset = Hackathon.objects.filter(
                    start__gt=current_date, end__gt=current_date)
            else:
                raise exceptions.ValidationError("Invalid query parameter!")
        return queryset


class HackathonsRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    API used to read, update or delete the hackathon objects by their id.
    Only the Super User has the permissions to update or delete hackathon objects.
    """

    permission_classes = [HackathonPermissions]
    serializer_class = HackathonDetailSerializer
    lookup_field = 'slug'
    queryset = Hackathon.objects.all()


class HackathonSubmissionView(generics.ListCreateAPIView):
    """
    API to handle GET and POST for submission. For GET method:
    (i) Superuser can get all submissions (in any case).
    (ii) For ongoing hackathon authenticated users will get submissions of their team.
    (iii) For ongoing hackathon unauthenticated users will get ERROR 401 Unauthorized.
    (iv) If hackathon is not ongoing then anyone(even unauthenticated) will get all the submissions.
    """
    serializer_class = SubmissionsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return None
        try:
            hackathon = Hackathon.objects.get(slug=self.kwargs['slug'])
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound("Hackathon does not exists!")
        else:
            user = self.request.user
            if hackathon.status == "Ongoing":
                if user.is_authenticated:
                    if user.is_superuser:
                        return Submission.objects.filter(hackathon=hackathon)
                    else:
                        try:
                            team = Team.objects.get(members=user, hackathon=hackathon)
                        except Team.DoesNotExist:
                            raise exceptions.NotFound("Team does not exists!")
                        else:
                            return Submission.objects.filter(hackathon=hackathon, team=team)
                else:
                    raise exceptions.NotAuthenticated(detail="Authentication is required to get submissions of ongoing hackathon!")
            else:
                return Submission.objects.filter(hackathon=hackathon)

    def create(self, request, *args, **kwargs):
        try:
            hackathon = Hackathon.objects.get(slug=self.kwargs['slug'])
            # The default score should remain zero
            # even if user has passed any other value
            if 'score' in request.data:
                request.data['score'] = 0
            if hackathon.status != "Ongoing":
                return Response("Submissions can only be made to Ongoing Hackathons", status=status.HTTP_400_BAD_REQUEST)
            team = Team.objects.get(members=request.user, hackathon=hackathon)
            if request.data['team'] != team.team_id:
                return Response("You can make submission only for your team", status=status.HTTP_400_BAD_REQUEST)
            submission = Submission.objects.filter(
                team=team, hackathon=hackathon)
            if len(submission):
                return Response("A Submission Already Exists!", status=status.HTTP_400_BAD_REQUEST)
            # As we are using id as pk for hackathon, and slug for routing
            # so due to foreign key constraints we need to change request data to contain hackathon pk.
            #Similar reason for team.
            request.data['hackathon'] = hackathon.pk
            request.data['team'] = team.pk

        except Hackathon.DoesNotExist:
            raise exceptions.NotFound("Hackathon does not exist!")
        except Team.DoesNotExist:
            raise exceptions.NotFound("Team does not exist!")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TeamView(generics.RetrieveUpdateDestroyAPIView):
    """
    API used to read, update or delete the Team objects by their team_id. Only the Super User has the permissions to delete Team objects.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated(), IsLeaderOrSuperUser()]

    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    lookup_field = 'team_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        leader = ProfileSerializer(instance.leader).data
        members = ProfileSerializer(instance.members, many=True).data
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['leader'] = leader
        data['members'] = members
        return Response(data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        leader = ProfileSerializer(instance.leader).data
        members = ProfileSerializer(instance.members, many=True).data
        data = serializer.data
        data['leader'] = leader
        data['members'] = members

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data)

class MemberExitView(generics.GenericAPIView):
    """
    Allows only leader to remove any team member.
    Team members can exit but cannot remove others.
    Leader cannot exit team. If leader wants to leave he has to delete the team.
    """

    serializer_class = MemberExitSerializer
    queryset = Team.objects.all()
    lookup_field = 'team_id'
    permission_classes = [permissions.IsAuthenticated]
    def get_serializer_context(self):
        return {
            'request': self.request,
            'kwargs': self.kwargs
        }

    def patch(self, request, **kwargs):
        serializer = self.get_serializer()
        serializer.exit_team()
        return Response("Successfully removed from the team",status=status.HTTP_200_OK)

class SubmissionRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    API used to read, update and delete the particular submissions of particular hackathon.
    """
    serializer_class = SubmissionRUDSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return None

        queryset = Submission.objects.filter(id=self.kwargs['id'])
        user = self.request.user
        if queryset:
            hackathon = Hackathon.objects.get(id=queryset[0].hackathon_id)
            if hackathon.status == 'Completed':
                if self.request.method == 'GET':
                    return queryset
                elif self.request.method == 'DELETE' or self.request.method == 'PUT' or self.request.method == 'PATCH':
                    try:
                        team = Team.objects.get(members=user, hackathon=hackathon)
                        return queryset
                    except Team.DoesNotExist:
                        raise exceptions.PermissionDenied(detail="Not the member of registered Team")
            elif hackathon.status == 'Ongoing':
                if not user:
                    raise exceptions.PermissionDenied(detail="Must be Logged in to view ongoing submissions")
                try:
                    team = Team.objects.get(members=user, hackathon=hackathon)
                    return queryset
                except Team.DoesNotExist:
                    raise exceptions.PermissionDenied(detail="Not the member of registered Team")
            else:
                raise exceptions.PermissionDenied(detail="Hackathon is not started yet")
        else:
            raise exceptions.NotFound("Submission does not exist!")
