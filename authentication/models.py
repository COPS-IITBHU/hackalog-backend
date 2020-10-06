from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
  uid = models.CharField(max_length=64, primary_key=True, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  name=models.CharField(max_length=255)
  email=models.EmailField(max_length=255)
  # github_handle=models.CharField(max_length=255)

  def __str__(self):
    return self.name