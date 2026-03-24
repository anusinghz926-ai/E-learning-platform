from django.urls import path
from .views import analytics_dashboard, teacher_dashboard, admin_dashboard

urlpatterns = [
    # 🔥 Analytics (Main Dashboard)
    path('', analytics_dashboard, name='analytics'),

    # 🔥 Teacher Dashboard
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),

    # 🔥 NEW ADMIN DASHBOARD (User Management)
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]