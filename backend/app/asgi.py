import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django_asgi_app = get_asgi_application()

# This has to be called after get_asgi_application because django isn't done with the setups yet
from app.token_authentication_middleware import TokenAuthMiddleware
import game.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(URLRouter(game.routing.websocket_urlpatterns))
    ),
})