from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import User
from apps.courses.models import Course
from apps.payments.models import Purchase
from .models import CourseView


# 🔥 ADMIN DASHBOARD
@login_required
def analytics_dashboard(request):
    return render(request, 'admin_panel/analytics.html', {
        'students': User.objects.filter(user_type='student').count(),
        'teachers': User.objects.filter(user_type='teacher').count(),
        'courses': Course.objects.count(),
        'sales': Purchase.objects.filter(is_paid=True).count(),
        'views': CourseView.objects.all()
    })


# 🔥 TEACHER DASHBOARD
@login_required
def teacher_dashboard(request):

    # Only allow teachers
    if request.user.user_type != 'teacher':
        return render(request, 'error.html', {'message': 'Access Denied'})

    # Purchases of teacher's courses
    purchases = Purchase.objects.filter(
        course__teacher=request.user,
        is_paid=True
    )

    # Total earnings
    total_earnings = sum(p.course.price for p in purchases)

    # Unique students
    total_students = purchases.values('student').distinct().count()

    # Total sales
    total_sales = purchases.count()

    # Teacher courses
    my_courses = Course.objects.filter(teacher=request.user)

    return render(request, 'teachers/dashboard.html', {
        'purchases': purchases,
        'total_earnings': total_earnings,
        'total_students': total_students,
        'total_sales': total_sales,
        'courses': my_courses
    })