from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from .serializers import HackathonSerializer
from .models import Hackathon
from .permissions import HackathonPermissions

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
