from .models import CourseView

def increase_view(course):
    obj, created = CourseView.objects.get_or_create(course=course)
    obj.views += 1
    obj.save()