from .models import Hackathon
from rest_framework import serializers
from authentication.models import User

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ['title','start','end','image','results_declared','max_team_size','slug']
