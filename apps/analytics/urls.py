from django.urls import path
from .views import analytics_dashboard, teacher_dashboard

urlpatterns = [
    path('', analytics_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
]