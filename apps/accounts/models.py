from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    USER_TYPE = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE,
        default='student'
    )

    # 🔥 NEW: BLOCK USER FEATURE
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username