from django.urls import path, re_path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def ping(request):
  return Response("Hello I'm chat helper service version 1")

urlpatterns = [
    path('auth/', include("chat.api.v1.auth.urls")),
    path('upload/', include("chat.api.v1.upload.urls")),
    path('worker/', include("chat.api.v1.worker.urls")),
]