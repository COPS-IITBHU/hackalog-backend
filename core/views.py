from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils import timezone
import pytz
from .models import Hackathon
from .serializers import HackathonTeamListSerializer, HackathonTeamCreateSerializer,HackathonSerializer

from .serializers import HackathonSerializer
from .permissions import HackathonPermissions

class HackathonTeamCreateView(generics.CreateAPIView):
    """
    post:
    Create a team to participate in a Hackathon.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HackathonTeamCreateSerializer

    def post(self, reqeuest):
        serializer = self.get_serializer(data=reqeuest.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

class HackathonTeamListView(generics.RetrieveAPIView):
    """
    Returns list of teams participating in a particular hackathon
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = HackathonTeamListSerializer
    lookup_field = 'pk'
    queryset = Hackathon.objects.all()

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
                return Response("Invalid query parameter", status.HTTP_400_BAD_REQUEST)
        return queryset

class HackathonCreateView(generics.CreateAPIView):
    '''
    API used to create hackathon objects. Can only be accessed by the Super User
    '''
    serializer_class = HackathonSerializer
    permission_classes = [permissions.IsAdminUser]

class HackathonsRUDView(generics.RetrieveUpdateDestroyAPIView):
    '''
    API used to read, update or delete the hackathon objects by their id. Only the Super User has the permissions to update or delete hackathon objects.
    '''

    permission_classes = [HackathonPermissions]
    serializer_class = HackathonSerializer
    lookup_field = 'pk'
    queryset = Hackathon.objects.all()
