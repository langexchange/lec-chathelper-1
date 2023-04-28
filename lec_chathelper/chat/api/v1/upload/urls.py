from django.urls import path, re_path, include
from .views import *


urlpatterns = [
    re_path(r'^(?P<path>.*)/(?P<filename>[^/]*)$', FileUploadView.as_view()),
    path('ping', ping)
]