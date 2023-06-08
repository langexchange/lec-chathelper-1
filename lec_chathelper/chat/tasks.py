from celery import shared_task
import environ
from .chatworker import ChatWorkerConsumer
from .chatworker.handlers import UserUpdateHandler, FriendStateHandler
import logging
from celery.contrib.abortable import AbortableTask
from lec_chathelper.settings import BASE_DIR

# logger = get_task_logger(__name__)
  
logger = logging.getLogger(__name__)
count = 0


def initConsumers(task_id):
  import threading, os
  logger.info("Chat consumer %d get initialized %s at thread %d by process %d %s", count, __name__, threading.get_ident() ,os.getpid(), "requested by task id {}".format(task_id))

  env = environ.Env()
  environ.Env.read_env(os.path.join(BASE_DIR,'env/.dev.env'))
  APP_BROKERS = env('APP_BROKERS')

  # TODO: SHOULD HAVE A UNIQUE CONFIG FILE AS IT IS LARGER
  conf = {'bootstrap.servers': APP_BROKERS,
      'group.id': "chathelper1",
      'auto.offset.reset': 'earliest',
      'enable.auto.commit': False}  
  consumer = ChatWorkerConsumer(5,conf)
  consumer.register("chathelper-friendstate", FriendStateHandler)
  consumer.register("chathelper-userinfo", UserUpdateHandler)
  
  # TODO: Catch exeption from here

  logger.info("START CONSUMER LOOP to listen {}: ...".format(APP_BROKERS) )
  consumer.initPullLoop(task_id)

     


@shared_task(ignore_result=True, bind=True, base=AbortableTask)
def startChatWorker(self):
    import os, threading
    global count
    count = count + 1
    logger.info("Init chat consumer %d  %s at thread %d at process id %d %s ", count, __name__, threading.get_ident() ,os.getpid(), "requested by task id {}".format(self.request.id))

    thread = threading.Thread(target=initConsumers, args=(self.request.id,))
    thread.daemon = True
    thread.start()

# @shared_task
# def add(x, y):
#     logger.info('Found addition')
#     logger.info('Added {0} and {1} to result, '.format(x,y))
#     return x+y