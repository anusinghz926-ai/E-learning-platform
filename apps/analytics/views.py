from django.shortcuts import render
from apps.accounts.models import User
from apps.courses.models import Course
from apps.payments.models import Purchase
from .models import CourseView

def analytics_dashboard(request):
    return render(request, 'admin_panel/analytics.html', {
        'students': User.objects.filter(user_type='student').count(),
        'teachers': User.objects.filter(user_type='teacher').count(),
        'courses': Course.objects.count(),
        'sales': Purchase.objects.count(),
        'views': CourseView.objects.all()
    })