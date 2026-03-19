from django.urls import path
from .views import buy_course

urlpatterns = [
    path('buy/<int:course_id>/', buy_course, name='buy_course'),
]