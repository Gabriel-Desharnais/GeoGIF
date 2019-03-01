from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
import GeoGIF1.routing

application = ProtocolTypeRouter({
	'websocket': SessionMiddlewareStack(
		URLRouter(
			GeoGIF1.routing.websocket_urlpatterns
			)
		),
})

