from django.db import models
from apps.accounts.models import User

class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    video = models.FileField(upload_to='lectures/')
    notes = models.FileField(upload_to='notes/')
    created_at = models.DateTimeField(auto_now_add=True)
 
    is_active = models.BooleanField(default=True)  # ✅ NEW
    

    def __str__(self):
        return self.title