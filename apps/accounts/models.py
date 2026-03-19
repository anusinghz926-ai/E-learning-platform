from django.contrib.auth.models import AbstractUser
from django.db import models
AUTH_USER_MODEL = 'accounts.User'

class User(AbstractUser):
    USER_TYPE = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE)