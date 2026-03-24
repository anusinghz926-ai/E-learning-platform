from django.urls import path
from .views import (
    upload_course,
    search_courses,
    my_courses,
    edit_course,
    delete_course,
    teacher_toggle_course,
    toggle_course_status
)

urlpatterns = [
    path('upload/', upload_course, name='upload_course'),
    path('search/', search_courses, name='search'),
    path('my-courses/', my_courses, name='my_courses'),
    path('edit-course/<int:course_id>/', edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', delete_course, name='delete_course'),

    # 🔥 BOTH TOGGLES
    path('teacher-toggle/<int:course_id>/', teacher_toggle_course, name='teacher_toggle_course'),
    path('toggle-course/<int:course_id>/', toggle_course_status, name='toggle_course'),
]