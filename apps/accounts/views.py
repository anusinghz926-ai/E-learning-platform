from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import User

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']

        user = User.objects.create_user(
            username=username,
            password=password,
            user_type=user_type
        )
        return redirect('login')

    return render(request, 'auth/signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            if user.user_type == 'student':
                return redirect('student_dashboard')
            elif user.user_type == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('admin_dashboard')

    return render(request, 'auth/login.html')