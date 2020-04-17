from django.urls import re_path
from chat import consumers as chat_consumers
from draft import consumers as draft_consumers
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': URLRouter([
        re_path(r'ws/chat/(?P<room_name>\w+)/$', chat_consumers.ChatConsumer),
        re_path(r'ws/draft/(?P<room_id>\w+)/$', draft_consumers.DraftConsumer)
    ])
})

ASGI_APPLICATION = "banpick.routing.application"