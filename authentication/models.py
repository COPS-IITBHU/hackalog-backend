import json
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  with open('authentication/college_list.json') as f:
        college_json = json.load(f)
        COLLEGE_NAME = [(str(college["name"]), str(college["name"])) for college in college_json]

  college = models.TextField(choices=COLLEGE_NAME)
  uid = models.CharField(primary_key=True, max_length=64)
  username = models.CharField(default=None, unique=True, null=True, max_length=64)
  name=models.CharField(max_length=255)
  github_handle = models.CharField(max_length=255)
  bio = models.TextField()
  interests = models.TextField()

  USERNAME_FIELD = 'uid'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
    return self.uid