from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.courses.models import Course
from .models import Purchase

# 🔥 WEBSOCKET IMPORTS
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@login_required
def buy_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # 🔥 CHECK IF ALREADY PURCHASED
    already_bought = Purchase.objects.filter(
        student=request.user,
        course=course
    ).exists()

    if already_bought:
        messages.warning(request, "⚠️ You already purchased this course!")
        return redirect('/search/')

    # ✅ CREATE PURCHASE
    purchase = Purchase.objects.create(
        student=request.user,
        course=course,
        is_paid=True
    )

    # 🔥 CALCULATE UPDATED DATA
    purchases = Purchase.objects.filter(is_paid=True)

    total_sales = purchases.count()
    total_revenue = sum(p.course.price for p in purchases)

    # 🔥 SEND REAL-TIME DATA (WebSocket)
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "dashboard",
        {
            "type": "send_update",
            "data": {
                "sales": total_sales,
                "revenue": total_revenue,
            }
        }
    )

    # ✅ SUCCESS MESSAGE
    messages.success(request, "✅ Course purchased successfully!")

    return redirect('/search/')