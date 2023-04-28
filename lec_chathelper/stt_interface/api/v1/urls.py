from django.urls import path, include


urlpatterns = [
    path('general/', include("stt_interface.api.v1.general.urls")),
]