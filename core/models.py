from django.db import models
# Create your models here.

HACKATHON_STATUS_CHOICES = (
    ('U', 'upcoming'),
    ('F', 'finished'),
    ('C', 'cancelled'),
    ('O', 'ongoing')
)

class UserProfile(models.Model):
    """
      Dummy profile model actual model need to be imported from authentication app.
      Created because currently authentication pr is not merged. 
    """
    pass


class Hackathon(models.Model):
    """
      A model representing hackathon.
      `
        title = models.CharField(default="No title provided", max_length=100)
        date = models.DateField(auto_now=False, auto_now_add=False)
        time = models.TimeField(auto_now=False, auto_now_add=False)
        image = models.CharField(null=True, blank=True, max_length=200)
        organisers = models.ForeignKey(UserProfile, on_delete=models.SET_NULL)
        result = 1# to be decided.
        status = models.CharField(choices=HACKATHON_STATUS_CHOICES, max_length=1)
      `
    """
    title = models.CharField(default="No title provided",
                             max_length=100, unique=True)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    image = models.CharField(null=True, blank=True, max_length=200)
    organizers = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, related_name="hackathon_organizer")
    result = 1  # to be decided(Later).
    status = models.CharField(choices=HACKATHON_STATUS_CHOICES, max_length=1)

    def __str__(self):
        return self.title


class Team(models.Model):
    """
      A model representing a team.
      `
        name = models.CharField(required=True, max_length=50, validators=[unique_team_name_in_hackathon])
        leader = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
        hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
        team_id = models.CharField(required=True, max_length=50) # to be decided for making unique team ids.
        members = models.ManyToManyField(UserProfile, on_delete=models.CASCADE)
      `
    """
    name = models.CharField(blank=False, null=False, max_length=50)
    leader = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="team_leader")
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    team_id = models.CharField(blank=False, null=False, max_length=50)  # to be decided for making unique team ids.
    members = models.ManyToManyField(UserProfile, related_name="teams")

    def __str__(self):
        return self.name


class Link(models.Model):
    """
      A model representing a link.
      `
        location = models.CharField(max_length=200)
      `
    """
    location = models.CharField(max_length=200)

    def __str__(self):
        pass


class Submission(models.Model):
    """
      A model representing a submission for a hackathon.
      `
        team = models.ForeignKey(Team, on_delete=models.CASCADE)
        hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
        time = models.TimeField(auto_now=True, auto_now_add=True)
        score = models.IntegerField()
        links = models.ManyToManyField(Link, on_delete=models.CASCADE)
        description = models.TextField()
      `
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    time = models.TimeField(auto_now=True)
    score = models.IntegerField()
    links = models.ManyToManyField(Link)
    description = models.TextField()

    def __str__(self):
        return f'{self.team.name}\'s Submission'
