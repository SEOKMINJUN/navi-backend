
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='이메일')
    nickname = models.CharField(max_length=30, unique=True)
    student_id = models.CharField(max_length=30, unique=True)