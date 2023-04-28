from django.urls import path, re_path, include
from .v1 import ping

app_name = 'chat' #Template namespace
urlpatterns = [
    path('v1/', include("chat.api.v1.urls")),
    path('v1/ping', ping)
]