import os
import sys
from pathlib import Path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from chatApp import routing

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "conversa_dj"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digitalAPI.settings')

application = get_asgi_application()
 
from channels.routing import ProtocolTypeRouter, URLRouter 
 
 
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(routing.websocket_urlpatterns),
    }
)