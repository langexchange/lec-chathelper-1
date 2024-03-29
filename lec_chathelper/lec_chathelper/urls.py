"""lec_chathelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

open_url = [
  path('', include('django_prometheus.urls')),
]

private_url = [
  path('chat/', include('chat.api.urls')),
]

urlpatterns = [
    *open_url,
    *private_url,
    re_path(r'^$', get_schema_view(
        title="Vu Service API",
        description="API for service which Vu implements in LangExchange project",
        version="1.0.0",
        patterns=open_url
    ), name='openapi-schema'),

    path('swagger-ui/', TemplateView.as_view(
        template_name='gc_interface/index.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]

