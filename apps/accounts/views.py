from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from apps.payments.models import Purchase
from apps.courses.models import Course

User = get_user_model()


# =====================================================
# 👨‍🏫 TEACHER DASHBOARD
# =====================================================
@login_required
def teacher_dashboard(request):
    if request.user.user_type != 'teacher':
        return redirect('/')

    purchases = Purchase.objects.filter(
        course__teacher=request.user,
        is_paid=True
    )

    total_earnings = sum(p.course.price for p in purchases)
    total_students = purchases.values('student').distinct().count()
    total_sales = purchases.count()

    courses = Course.objects.filter(teacher=request.user)

    return render(request, 'teachers/dashboard.html', {
        'purchases': purchases,
        'total_earnings': total_earnings,
        'total_students': total_students,
        'total_sales': total_sales,
        'courses': courses
    })


# =====================================================
# 👨‍💼 ADMIN DASHBOARD
# =====================================================
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('/')

    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_sales = Purchase.objects.filter(is_paid=True).count()

    total_revenue = sum(
        p.course.price for p in Purchase.objects.filter(is_paid=True)
    )

    courses = Course.objects.all()

    return render(request, 'admin_panel/dashboard.html', {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'courses': courses
    })


# =====================================================
# 👥 MANAGE USERS
# =====================================================
@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect('/')

    users = User.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'users': users})


@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('/')

    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return redirect('/accounts/admin-panel/users/')

    user.delete()
    return redirect('/accounts/admin-panel/users/')


@login_required
def toggle_block_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('/')

    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return redirect('/accounts/admin-panel/users/')

    user.is_blocked = not user.is_blocked
    user.save()

    return redirect('/accounts/admin-panel/users/')


# =====================================================
# 🔐 LOGIN + ADMIN SIGNUP (UNLIMITED ADMINS)
# =====================================================
def user_login(request):

    # 👉 Prevent logged-in users from seeing login again
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/analytics/')
        elif request.user.user_type == 'teacher':
            return redirect('/analytics/teacher-dashboard/')
        else:
            return redirect('/search/')

    if request.method == 'POST':

        # =========================
        # 🔐 LOGIN
        # =========================
        if 'login' in request.POST:

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user:

                if user.is_blocked:
                    return render(request, 'login.html', {
                        'error': 'Your account has been blocked'
                    })

                login(request, user)

                if user.is_superuser:
                    return redirect('/analytics/')
                elif user.user_type == 'teacher':
                    return redirect('/analytics/teacher-dashboard/')
                else:
                    return redirect('/search/')

            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })


        # =========================
        # 📝 ADMIN SIGNUP
        # =========================
        elif 'signup' in request.POST:

            username = request.POST.get('signup_username')
            email = request.POST.get('signup_email')
            password = request.POST.get('signup_password')
            confirm = request.POST.get('signup_confirm')
            admin_code = request.POST.get('admin_code')

            # 🔐 SECURITY (CHANGE THIS VALUE)
            if admin_code != "ADMIN123":
                return render(request, 'login.html', {
                    'error': 'Invalid Admin Code'
                })

            # VALIDATIONS
            if password != confirm:
                return render(request, 'login.html', {
                    'error': 'Passwords do not match'
                })

            if User.objects.filter(username=username).exists():
                return render(request, 'login.html', {
                    'error': 'Username already exists'
                })

            # CREATE ADMIN
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            user.is_staff = True
            user.is_superuser = True
            user.user_type = 'admin'
            user.save()

            login(request, user)

            return redirect('/analytics/')

    return render(request, 'login.html')


# =====================================================
# 👨‍🎓 STUDENT LOGIN + SIGNUP
# =====================================================
def student_login(request):

    if request.method == 'POST':

        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user and user.user_type == 'student':

                if user.is_blocked:
                    return render(request, 'students/student_login.html', {
                        'error': 'Your account has been blocked'
                    })

                login(request, user)
                return redirect('/search/')

            return render(request, 'students/student_login.html', {
                'error': 'Invalid credentials'
            })


        elif 'signup' in request.POST:

            username = request.POST.get('signup_username')
            email = request.POST.get('signup_email')
            password = request.POST.get('signup_password')
            confirm = request.POST.get('signup_confirm')

            if password != confirm:
                return render(request, 'students/student_login.html', {
                    'error': 'Passwords do not match'
                })

            if User.objects.filter(username=username).exists():
                return render(request, 'students/student_login.html', {
                    'error': 'Username already exists'
                })

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.user_type = 'student'
            user.save()

            return render(request, 'students/student_login.html', {
                'success': 'Account created! Please login.'
            })

    return render(request, 'students/student_login.html')


# =====================================================
# 👨‍🏫 TEACHER LOGIN + SIGNUP
# =====================================================
def teacher_login(request):

    if request.method == 'POST':

        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user and user.user_type == 'teacher':

                if user.is_blocked:
                    return render(request, 'teachers/teacher_login.html', {
                        'error': 'Your account has been blocked'
                    })

                login(request, user)
                return redirect('/analytics/teacher-dashboard/')

            return render(request, 'teachers/teacher_login.html', {
                'error': 'Invalid teacher credentials'
            })


        elif 'signup' in request.POST:

            username = request.POST.get('signup_username')
            email = request.POST.get('signup_email')
            password = request.POST.get('signup_password')
            confirm = request.POST.get('signup_confirm')
            
            if password != confirm:
                return render(request, 'teachers/teacher_login.html', {
                    'error': 'Passwords do not match'
                })

            if User.objects.filter(username=username).exists():
                return render(request, 'teachers/teacher_login.html', {
                    'error': 'Username already exists'
                })

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.user_type = 'teacher'
            user.save()

            return render(request, 'teachers/teacher_login.html', {
                'success': 'Account created! Please login.'
            })

    return render(request, 'teachers/teacher_login.html')


# =====================================================
# 🚪 LOGOUT
# =====================================================
def user_logout(request):
    logout(request)
    return redirect('/accounts/admin-login/')


# =====================================================
# 🔍 SEARCH COURSES
# =====================================================
@login_required
def search_courses(request):
    query = request.GET.get('q')

    purchased_ids = list(
        Purchase.objects.filter(
            student=request.user,
            is_paid=True
        ).values_list('course_id', flat=True)
    )

    courses = Course.objects.filter(title__icontains=query) if query else Course.objects.all()

    return render(request, 'students/search.html', {
        'courses': courses,
        'purchased_courses': purchased_ids
    })


# =====================================================
# 📚 MY COURSES
# =====================================================
@login_required
def my_courses(request):
    purchases = Purchase.objects.filter(
        student=request.user,
        is_paid=True
    )

    return render(request, 'students/my_courses.html', {
        'purchases': purchases
    })


# =====================================================
# 📤 UPLOAD COURSE
# =====================================================
@login_required
def upload_course(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        video = request.FILES.get('video')
        notes = request.FILES.get('notes')

        if not description or description.strip() == "":
            description = "Default course description"

        Course.objects.create(
            teacher=request.user,
            title=title,
            description=description,
            price=price,
            video=video,
            notes=notes
        )

        return redirect('/analytics/teacher-dashboard/')

    return render(request, 'teachers/upload.html')