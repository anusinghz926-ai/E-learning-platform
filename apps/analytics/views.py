from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from apps.accounts.models import User
from apps.courses.models import Course
from apps.payments.models import Purchase
from .models import CourseView


# =========================================
# 📊 ANALYTICS DASHBOARD (ADMIN OVERVIEW)
# =========================================
@login_required
def analytics_dashboard(request):

    if not request.user.is_superuser:
        return render(request, 'error.html', {'message': 'Access Denied'})

    return render(request, 'admin_panel/analytics.html', {
        'students': User.objects.filter(user_type='student').count(),
        'teachers': User.objects.filter(user_type='teacher').count(),
        'courses': Course.objects.count(),   # ✅ ALL COURSES
        'sales': Purchase.objects.filter(is_paid=True).count(),
        'views': CourseView.objects.all()
    })


# =========================================
# 👨‍🏫 TEACHER DASHBOARD
# =========================================
@login_required
def teacher_dashboard(request):

    if request.user.user_type != 'teacher':
        return render(request, 'error.html', {'message': 'Access Denied'})

    # ✅ ONLY ACTIVE COURSES
    courses = Course.objects.filter(
        teacher=request.user,
        is_active=True
    )

    purchases = Purchase.objects.filter(
        course__teacher=request.user,
        is_paid=True
    ).select_related('course', 'student')

    total_sales = purchases.count()
    total_students = purchases.values('student').distinct().count()
    total_earnings = sum(p.course.price for p in purchases)

    return render(request, 'teachers/dashboard.html', {
        'courses': courses,
        'purchases': purchases,
        'total_earnings': total_earnings,
        'total_students': total_students,
        'total_sales': total_sales,
    })


# =========================================
# ⚡ ADMIN DASHBOARD (SHOW ALL COURSES)
# =========================================
@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return render(request, 'error.html', {'message': 'Access Denied'})

    UserModel = get_user_model()

    # 👥 USERS
    total_users = UserModel.objects.count()
    total_students = UserModel.objects.filter(user_type='student').count()
    total_teachers = UserModel.objects.filter(user_type='teacher').count()

    # ✅ SHOW ALL COURSES (ACTIVE + INACTIVE)
    courses = Course.objects.all()

    total_courses = courses.count()

    purchases = Purchase.objects.filter(is_paid=True).select_related('course', 'student')

    total_sales = purchases.count()
    total_revenue = sum(p.course.price for p in purchases)

    recent_purchases = purchases.order_by('-id')[:10]

    users = UserModel.objects.all()

    return render(request, 'admin_panel/admin_dashboard.html', {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'users': users,
        'recent_purchases': recent_purchases,
        'courses': courses   # ✅ SEND COURSES
    })