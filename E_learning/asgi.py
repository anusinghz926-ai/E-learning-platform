import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# 🔥 SET SETTINGS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_learning.settings')

# 🔥 IMPORTANT (ensures apps load properly)
django.setup()

# 🔥 IMPORT ROUTING AFTER SETUP
from apps.analytics.routing import websocket_urlpatterns


# 🚀 FINAL APPLICATION
application = ProtocolTypeRouter({

    # HTTP REQUESTS
    "http": get_asgi_application(),

    # WEBSOCKET REQUESTS
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})