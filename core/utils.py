from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError


@receiver(pre_save, sender=Team)
def unique_team_name_in_hackathon(sender, instance, *args, **kwargs):
    """
    Checks the uniqueness of team names in a hackathon.
    """
    hackathon = instance.hackthon
    already_existing_teams = Team.objects.filter(hackathon=hackathon)
    for team in already_existing_teams:
        if team.name == instance.name:
            raise ValidationError('Duplicate team names.')
          
