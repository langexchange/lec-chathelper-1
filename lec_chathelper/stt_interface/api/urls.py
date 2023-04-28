from django.urls import path, include
from .v1 import ping




app_name = 'stt_interface' #Template namespace
urlpatterns = [
    path('v1/', include("stt_interface.api.v1.urls")),
    path('v1/ping', ping),
]