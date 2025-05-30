
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    student_id = models.CharField(max_length=30, unique=True)