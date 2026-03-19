from django.urls import path
from .views import upload_course, search_course, my_courses

urlpatterns = [
    path('upload/', upload_course, name='upload_course'),
    path('search/', search_course, name='search'),
    path('my-courses/', my_courses, name='my_courses'),
]