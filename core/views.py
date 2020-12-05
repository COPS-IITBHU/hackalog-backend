from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Hackathon, Team, Submission
from .serializers import HackathonSerializer, TeamSerializer, TeamCreateSerializer, JoinTeamSerializer, SubmissionsSerializer
from .permissions import HackathonPermissions, AllowCompleteProfile


class HackathonTeamView(generics.ListCreateAPIView):
    """
    get:
    Returns a list of teams in a particular hackathon
    post:
    Creates a new team in a hackathon and return the team_id
    """
    permission_classes = [permissions.IsAuthenticated, AllowCompleteProfile]

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
            hackathon = Hackathon.objects.get(id=self.kwargs['pk'])
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound("Hackathon does not exist!")
        queryset = Team.objects.filter(hackathon=self.kwargs['pk'])
        return queryset

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JoinTeamView(generics.GenericAPIView):
    """
    patch:
    Join a team with team_id and hackathon_id
    """
    serializer_class = JoinTeamSerializer

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
    API used to read, update or delete the hackathon objects by their id. Only the Super User has the permissions to update or delete hackathon objects.
    """

    permission_classes = [HackathonPermissions]
    serializer_class = HackathonSerializer
    lookup_field = 'pk'
    queryset = Hackathon.objects.all()


class HackathonSubmissionView(generics.ListCreateAPIView):
    """
    API used to get the list of all the submissions of particular hackathon.
    """
    serializer_class = SubmissionsSerializer

    def get_permissions(self):
        return [permissions.AllowAny()]
        # try:
        #     hackathon = Hackathon.objects.get(id=self.kwargs['pk'])
        #     if self.request.method == 'GET' and hackathon.status!="Completed":
        #         return [permissions.IsAdminUser()]
        #     return [permissions.AllowAny()]
        # except Hackathon.DoesNotExist:
        #     raise exceptions.NotFound("Hackathon does not exist!")

    def get_queryset(self, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return None
        try:
            hackathon = Hackathon.objects.get(id=self.kwargs['pk'])
            user = self.request.user
            if hackathon.status!="Completed" and not self.request.user.is_superuser:
                try:
                    team = Team.objects.get(members=user, hackathon= hackathon)
                except:
                    raise exceptions.NotFound("Team does not exist!")
                queryset=Submission.objects.filter(team=team)
                return queryset
            queryset = Submission.objects.filter(hackathon=self.kwargs['pk'])
            return queryset
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound("Hackathon does not exist!")

