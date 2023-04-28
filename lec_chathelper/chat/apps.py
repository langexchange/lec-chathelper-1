from django.apps import AppConfig
from celery.exceptions import OperationalError
import logging


logger = logging.getLogger(__name__)

class ChatConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'chat'
