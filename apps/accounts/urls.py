from django.urls import path
from .views import (
    signup,
    user_login,
    user_logout,
    student_login,
    teacher_login
)

urlpatterns = [
    # 🔐 Common (optional)
    path('login/', user_login, name='login'),

    # 👨‍🎓 Student
    path('student-login/', student_login, name='student_login'),

    # 👨‍🏫 Teacher
    path('teacher-login/', teacher_login, name='teacher_login'),

    # 📝 Signup
    path('signup/', signup, name='signup'),

    # 🚪 Logout
    path('logout/', user_logout, name='logout'),
]