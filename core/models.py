from django.db import models
from authentication.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone
# Create your models here.


class Hackathon(models.Model):
    """
    A model representing a Hackathon
    """
    title = models.CharField(max_length=100, unique=True)
    tagline = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=400, default='')
    start = models.DateTimeField(auto_now_add=False)
    end = models.DateTimeField(auto_now_add=False)
    image = models.CharField(null=True, blank=True, max_length=200)
    results_declared = models.BooleanField(default=False)
    max_team_size = models.IntegerField(default=10)
    slug = models.SlugField()

    @property
    def status(self):
        current_date = timezone.now()
        if self.start<=current_date and self.end<=current_date :
            return "Completed"
        elif self.start<=current_date and self.end>=current_date :
            return "Ongoing"
        else:
            return "Upcoming"


    def __str__(self):
        return self.title


class Team(models.Model):
    """
    A model representing a participating team.
    """
    name = models.CharField(blank=False, null=False, max_length=50)
    leader = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="teams_as_a_leader")
    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="participating_teams")
    team_id = models.CharField(max_length=16, unique=True)
    members = models.ManyToManyField(User, related_name="teams_as_a_member")

    class Meta:
        unique_together = ("name", "hackathon")

    @property
    def score(self):
        if(self.hackathon.status!="Completed"):
            return "NA"
        return self.submission.score

    def __str__(self):
        return self.name


class Submission(models.Model):
    """
    A model representing submission for a hackthon.
    """
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(100)])
    description = models.TextField()

    def __str__(self):
        return f'{self.team.name}\'s Submission'


class Link(models.Model):
    """
    A model to hold link for refrences and resources for a submission.
    """
    url = models.URLField(max_length=200)
    title = models.CharField(default="No title provided.", max_length=100)
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="links")

    def __str__(self):
        return self.title
