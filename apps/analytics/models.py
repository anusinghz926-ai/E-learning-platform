from django.db import models
from apps.courses.models import Course

class CourseView(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)