from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def ping(request):
  return Response("Hello I'm chat helper service version 1")