from django.contrib import admin
from .models import Hackathon, Submission, Team
admin.site.register(Hackathon)
admin.site.register(Submission)

class TeamsPageAdmin(admin.ModelAdmin):
    list_display = ('name','hackathon',)

admin.site.register(Team, TeamsPageAdmin)
