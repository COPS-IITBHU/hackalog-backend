from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Hackathon, Team
from .serializers import HackathonSerializer, TeamSerializer, TeamCreateSerializer
from .permissions import HackathonPermissions, AllowCompleteProfile

class HackathonTeamView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, AllowCompleteProfile]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeamSerializer
        else:
            return TeamCreateSerializer

    def get_queryset(self, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return None
        try:
            return Hackathon.objects.get(id=self.kwargs['pk'])
        except Hackathon.DoesNotExist:
            raise exceptions.NotFound("Hackathon does not exist!")
        queryset = Team.objects.filter(hackathon=self.kwargs['pk'])
        return queryset

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
                queryset = Hackathon.objects.filter(start__lt=current_date, end__gt=current_date)
            elif(query == 'completed'):
                queryset = Hackathon.objects.filter(start__lt=current_date, end__lt=current_date)
            elif(query == 'upcoming'):
                queryset = Hackathon.objects.filter(start__gt=current_date, end__gt=current_date)
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
