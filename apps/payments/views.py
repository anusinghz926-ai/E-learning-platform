from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from apps.courses.models import Course
from .models import Purchase

@login_required
def buy_course(request, id):
    course = Course.objects.get(id=id)

    Purchase.objects.create(
        student=request.user,
        course=course,
        is_paid=True
    )

    return redirect('/my-courses/')