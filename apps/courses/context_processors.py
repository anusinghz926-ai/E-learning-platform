from .models import Course

def chatbot_courses(request):
    try:
        courses = list(
            Course.objects.all().values(
                'id', 'title', 'price', 'description'
            )
        )
    except:
        courses = []

    return {
        'chatbot_courses': courses
    }