from django.shortcuts import redirect
from apps.payments.models import Purchase
from apps.courses.models import Course

def buy_course(request, id):
    course = Course.objects.get(id=id)

    Purchase.objects.create(
        student=request.user,
        course=course,
        amount=course.price
    )

    return redirect('search')