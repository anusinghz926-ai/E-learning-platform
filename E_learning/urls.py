from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.courses.views import home   # 🔥 IMPORT HOME VIEW

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ HOME PAGE
    path('', home, name='home'),

    # ✅ APPS
    path('accounts/', include('apps.accounts.urls')),
    path('payments/', include('apps.payments.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('', include('apps.courses.urls')),   # keep this AFTER home
]

# ✅ MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)