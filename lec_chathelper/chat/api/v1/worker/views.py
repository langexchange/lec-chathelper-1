from chat.tasks import startChatWorker
from rest_framework.decorators import api_view
from chat.chatworker.handlers import *
import logging
from rest_framework.response import Response
from rest_framework import status
from lec_chathelper.celery import app as celery_app
from celery.contrib.abortable import AbortableAsyncResult

logger = logging.getLogger(__name__)

# 'stop/<int:task_id>'
@api_view(['GET'])
def deleteWorkerWithTask(request):
  if "task_id" not in request.query_params:
    return Response({
        "status": "fail",
        "message": "Missing task_id param to delete"
    }, status=status.HTTP_403_FORBIDDEN)
  
  task_id = request.query_params["task_id"]
  logger.info("Revoke task {} of chat consumer".format(task_id))
  #  1. Using "control.revoke" method
  # celery_app.control.revoke(task_id, terminate=True, signal='SIGKILL')
  #  2. Using AbortableAsyncResult 
  AbortableAsyncResult(id=task_id).abort()


  return Response({
        "status": "success",
        "message": "Remember that you have revoked a chat consumer with id {}. If this id is wrong, another task assigned this id will not execute at all".format(task_id)
    }, status = status.HTTP_201_CREATED)



@api_view(['GET'])
def startWorker(request):
  async_task = startChatWorker.delay()
  return Response({
     "status": "success",
     "message": "The consumer task is sent with task id {}".format(async_task.task_id),
     "payload": {
      "task_id": async_task.task_id,
     },
  }, status = status.HTTP_201_CREATED)



@api_view(['GET'])
def ping(request):
  return Response({
     "status": "success",
     "message": "Hello I'm chat worker api"}, status = status.HTTP_201_CREATED)
    