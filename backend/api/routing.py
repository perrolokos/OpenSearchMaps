from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/map/(?P<map_id>\d+)/$", consumers.KnowledgeMapConsumer.as_asgi()),
]
