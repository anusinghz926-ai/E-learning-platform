from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required
from apps.payments.models import Purchase

# 👨‍🏫 TEACHER DASHBOARD
@login_required
def teacher_dashboard(request):

    # 🔐 SECURITY CHECK
    if request.user.user_type != 'teacher':
        return redirect('/')   # or show error page

    purchases = Purchase.objects.filter(
        course__teacher=request.user,
        is_paid=True
    )

    total_earnings = sum([p.course.price for p in purchases])
    total_students = purchases.values('student').distinct().count()
    total_sales = purchases.count()

    return render(request, 'teachers/dashboard.html', {
        'purchases': purchases,
        'total_earnings': total_earnings,
        'total_students': total_students,
        'total_sales': total_sales,
    })


# 👨‍💼 ADMIN DASHBOARD
@login_required
def admin_dashboard(request):

    # 🔐 SECURITY CHECK
    if not request.user.is_superuser:
        return redirect('/')

    from django.contrib.auth import get_user_model
    from apps.courses.models import Course

    User = get_user_model()

    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_sales = Purchase.objects.filter(is_paid=True).count()

    return render(request, 'admin_panel/dashboard.html', {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_sales': total_sales,
    })


def signup(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            user_type=request.POST['user_type']
        )
        return redirect('/accounts/login/')
    
    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)

            if user.user_type == 'teacher':
                return redirect('/analytics/teacher-dashboard/')
            elif user.user_type == 'student':
                return redirect('/search/')
            else:
                return redirect('/analytics/')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/accounts/login/')

def student_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user and user.user_type == 'student':
            login(request, user)
            return redirect('/search/')
        else:
            return render(request, 'student_login.html', {'error': 'Invalid student credentials'})

    return render(request, 'students/student_login.html')

# 👨‍🏫 TEACHER LOGIN
def teacher_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user and user.user_type == 'teacher':
            login(request, user)
            return redirect('/analytics/teacher-dashboard/')
        else:
            return render(request, 'teacher_login.html', {'error': 'Invalid teacher credentials'})

    return render(request, 'teachers/teacher_login.html') 
@login_required
def search_courses(request):

    if request.user.user_type != 'student':
        return redirect('/')

    # your logic here