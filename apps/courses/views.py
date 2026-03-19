from django.shortcuts import render, redirect
from apps.courses.models import Course
from apps.payments.models import Purchase
from apps.analytics.utils import increase_view


# 📌 Course Detail
def course_detail(request, id):
    course = Course.objects.get(id=id)

    increase_view(course)  # 🔥 Track views

    return render(request, 'course_detail.html', {'course': course})


# 📌 Student Search
def search_course(request):
    query = request.GET.get('q')

    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()

    return render(request, 'students/search.html', {'courses': courses})


# 📌 My Courses (Student)
def my_courses(request):
    purchases = Purchase.objects.filter(student=request.user, is_paid=True)
    return render(request, 'students/my_courses.html', {'purchases': purchases})


# 📌 Teacher Upload
def upload_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        video = request.FILES.get('video')
        notes = request.FILES.get('notes')

        Course.objects.create(
            teacher=request.user,
            title=title,
            description=description,
            price=price,
            video=video,
            notes=notes
        )
        return redirect('search')  # redirect after upload

    return render(request, 'teachers/upload.html')