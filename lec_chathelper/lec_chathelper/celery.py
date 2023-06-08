import os
from celery import Celery
import logging
import logging.config
import yaml
import environ
import os 
from lec_chathelper.settings import BASE_DIR
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR,'env/.dev.env'))

LOG_FILE_FROM_ROOT = env("LOG_FILE_FROM_ROOT")

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lec_chathelper.settings')

# TODO: Create a configuration for Celery
app = Celery('lec_chathelper')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# Logging configuration

with open(os.path.join(BASE_DIR,'chat/chatworker/conf/logging.yml'), "r") as file:
  try:
    config=yaml.safe_load(file)
  except yaml.YAMLError as e:
    raise("Error while parsing YAML config file")

config["handlers"]["file-handler"]["filename"] = os.path.join(BASE_DIR, LOG_FILE_FROM_ROOT)
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

# logger = get_task_logger(__name__)
logger.info("Celery process id %s",os.getpid())

@app.task(bind=True)
def debug_task(self):
    print(f'Request HELLO: {self.request!r}')
