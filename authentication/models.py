from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  uid = models.CharField(primary_key=True, max_length=64)
  username = models.CharField(unique=True, max_length=64)
  name=models.CharField(max_length=255)
  college = models.CharField(max_length=255)
  github_handle = models.CharField(max_length=255,blank=True)
  bio = models.TextField(blank=True)
  interests = models.TextField(blank=True)

  USERNAME_FIELD = 'uid'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
    return self.name