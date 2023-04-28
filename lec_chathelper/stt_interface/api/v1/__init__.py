from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def ping(request):
  return Response("Hello I'm grammar correction service version 1")