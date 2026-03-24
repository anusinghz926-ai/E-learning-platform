from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.user_login, name='login'),
    path('student-login/', views.student_login, name='student_login'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('admin-login/', views.user_login, name='admin_login'),

    path('logout/', views.user_logout, name='logout'),

    path('admin-panel/users/', views.manage_users, name='manage_users'),
    path('admin-panel/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-panel/block-user/<int:user_id>/', views.toggle_block_user, name='block_user'),
]