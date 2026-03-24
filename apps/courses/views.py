from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.courses.models import Course
from apps.payments.models import Purchase
from apps.analytics.utils import increase_view


# ✏️ EDIT COURSE
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    if request.method == "POST":
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.price = request.POST.get('price')

        if request.FILES.get('video'):
            course.video = request.FILES.get('video')

        if request.FILES.get('notes'):
            course.notes = request.FILES.get('notes')

        course.save()
        return redirect('/analytics/teacher-dashboard/')

    return render(request, 'teachers/edit_course.html', {'course': course})


# ❌ SOFT DELETE
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    course.is_active = False
    course.save()

    return redirect('/analytics/teacher-dashboard/')


# 📌 COURSE DETAIL
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    if not course.is_active:
        return render(request, 'error.html', {'message': 'Course not available'})

    increase_view(course)

    return render(request, 'course_detail.html', {'course': course})


# 🔍 SEARCH (ONLY ACTIVE)
@login_required
def search_courses(request):
    query = request.GET.get('q')

    if query:
        courses = Course.objects.filter(title__icontains=query, is_active=True)
    else:
        courses = Course.objects.filter(is_active=True)

    purchased_courses = list(
        Purchase.objects.filter(
            student=request.user,
            is_paid=True
        ).values_list('course_id', flat=True)
    )

    return render(request, 'students/search.html', {
        'courses': courses,
        'purchased_courses': purchased_courses
    })


# 📚 STUDENT COURSES
@login_required
def my_courses(request):
    purchases = Purchase.objects.filter(student=request.user, is_paid=True)
    return render(request, 'students/my_courses.html', {'purchases': purchases})


# 📤 UPLOAD COURSE
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
            notes=notes,
            is_active=True
        )

        return redirect('/analytics/teacher-dashboard/')

    return render(request, 'teachers/upload.html')


# 🏠 HOME
def home(request):
    return render(request, 'home.html')
from django.contrib.auth.decorators import login_required

@login_required
def teacher_toggle_course(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user   # 🔥 ONLY OWN COURSE
    )

    course.is_active = not course.is_active
    course.save()

    return redirect('/analytics/teacher-dashboard/')

# ⚡ ADMIN TOGGLE (ALL COURSES)
@login_required
def toggle_course_status(request, course_id):
    if not request.user.is_superuser:
        return redirect('/')

    course = get_object_or_404(Course, id=course_id)

    course.is_active = not course.is_active
    course.save()

    return redirect('/analytics/admin-dashboard/')