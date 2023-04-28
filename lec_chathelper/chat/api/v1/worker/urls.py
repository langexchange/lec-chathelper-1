from django.urls import path, include
from .views import deleteWorkerWithTask, startWorker, ping

urlpatterns = [
    path('start', startWorker),
    path('stop', deleteWorkerWithTask),
    path('ping', ping),
]