from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  name=models.CharField(max_length=255)
  handle = models.CharField(max_length=255, null=True)
  college = models.CharField(max_length=255)
  github_handle = models.CharField(max_length=255,blank=True)
  bio = models.TextField(max_length=255,blank=True)
  interests = models.TextField(max_length=255,blank=True)

  def __str__(self):
    return self.name