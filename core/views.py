from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Hackathon, Team
from .serializers import HackathonTeamCreateSerializer, HackathonSerializer, TeamSerializer
from .permissions import HackathonPermissions, isProfileComplete

class HackathonTeamView(generics.GenericAPIView):
    # Required for POST request
    serializer_class = HackathonTeamCreateSerializer
    permission_classes = [isProfileComplete]

    # To over-write get_queryset, removes AssertionError
    def get_queryset(self):
        return

    def post(self, request, *args, **kwargs):
        """
        Users with completed profile can create a team with POST request
        """
        if request.data['hackathon'] != kwargs['pk']:
            raise exceptions.ValidationError("Hackathon ID does not match in URL and Request body!")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """
        Returns list of team registered for a hackathon
        """
        try:
            if Hackathon.objects.get(id=kwargs['pk']) is not None:
                queryset = Team.objects.filter(hackathon=kwargs['pk'])
        except:
            return Response("Hackathon does not exist!", status=status.HTTP_404_NOT_FOUND)
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

query_param = openapi.Parameter('query', openapi.IN_QUERY, description="Query parameter - 'upcoming', 'ongoing' or 'completed'",
                                type=openapi.TYPE_STRING)
@method_decorator(name="get", decorator=swagger_auto_schema(manual_parameters=[query_param]))
class HackathonListView(generics.ListAPIView):
    """
    Returns list of Hackathons according to query parameter.
    ongoing:
    List of ongoing Hackathons
    upcoming:
    List of upcoming Hackathons
    completed:
    List of completed Hackathons
    """
    serializer_class = HackathonSerializer
    permission_classes = [permissions.AllowAny]

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

class HackathonCreateView(generics.CreateAPIView):
    """
    API used to create hackathon objects. Can only be accessed by the Super User
    """
    serializer_class = HackathonSerializer
    permission_classes = [permissions.IsAdminUser]

class HackathonsRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    API used to read, update or delete the hackathon objects by their id. Only the Super User has the permissions to update or delete hackathon objects.
    """

    permission_classes = [HackathonPermissions]
    serializer_class = HackathonSerializer
    lookup_field = 'pk'
    queryset = Hackathon.objects.all()
