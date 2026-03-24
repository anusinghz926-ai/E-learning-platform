from django.db import models
from django.conf import settings
from apps.courses.models import Course

User = settings.AUTH_USER_MODEL  # 🔥 BEST PRACTICE

class Purchase(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # 💳 Payment info
    is_paid = models.BooleanField(default=False)

    # 🔥 Prevent duplicate purchase
    class Meta:
        unique_together = ('student', 'course')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course}"