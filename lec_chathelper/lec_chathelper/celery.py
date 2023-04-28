import os
from celery import Celery
import logging
import logging.config
import yaml
import environ
import os 

env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR,'env/.dev.env'))

LOG_FILE = env("LOG_FILE")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

config["handlers"]["file-handler"]["filename"] = LOG_FILE
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

# logger = get_task_logger(__name__)
logger.info("Celery process id %s",os.getpid())

@app.task(bind=True)
def debug_task(self):
    print(f'Request HELLO: {self.request!r}')
