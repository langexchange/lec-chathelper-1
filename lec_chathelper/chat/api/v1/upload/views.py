from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import FileResponse
from datetime import datetime
import hmac
import hashlib
import os
import environ
import boto3
from botocore.exceptions import ClientError
import mimetypes
from lec_chathelper.settings import BASE_DIR

env = environ.Env()
# TODO: Modify this using sys.path
environ.Env.read_env(os.path.join(BASE_DIR,'env/.dev.env'))


## s3 bucket initialize
S3_ACCESS_KEY = env("S3_ACCESS_KEY")
S3_SECRET_KEY = env("S3_SECRET_KEY")
S3_BUCKET = env("S3_BUCKET")
XMPP_UPLOAD_KEY = env("XMPP_UPLOAD_KEY")

s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)


@api_view(['GET', 'POST'])
def ping(request):
  return Response("Hello I'm chat helper service")

# Create your views here.
class FileUploadView(APIView):
   """
    Views to update file to S3
    # PUT /chat/upload/filepath/filename?v2=auth_token 
    # HEAD /chat/upload/filepath/filename
    # GET /chat/upload/filepath/filename 
   """
   parser_classes = [FileUploadParser]

   def get(self, request, path, filename, format=None):
      CONTENT_TYPE = mimetypes.guess_type(filename)[0] or ''
      IF_NONE_MATCH = request.META.get("IF_NONE_MATCH")
      IF_MODIFIED_SINCE = request.META.get("IF_MODIFIED_SINCE")
      last_modified_date = datetime(1, 1, 1)
      if IF_MODIFIED_SINCE:
        last_modified_date = datetime.strptime(IF_MODIFIED_SINCE, "%a, %d %b %Y %H:%M:%S %Z")
      

      #Check content type header
      try:
        s3_response = s3_client.get_object(Bucket=S3_BUCKET, IfNoneMatch=IF_NONE_MATCH or '', IfModifiedSince=last_modified_date, Key=f'langchat/{path}/{filename}')

      except s3_client.exceptions.NoSuchKey:
        return Response({
           "status": "fail",
           "message": "There is no file having such path"
        }, status=status.HTTP_400_BAD_REQUEST)
      except s3_client.exceptions.InvalidObjectState as e:
         return Response({
           "status": "fail",
           "message": f"{e}"
        }, status=status.HTTP_400_BAD_REQUEST)
      
      headers = {
        "Last-Modified": s3_response['LastModified'],
        "Content-Length": s3_response['ContentLength'],
        "ETag": s3_response['ETag'],
        "Cache-Control": s3_response.get('CacheControl', ''),
        "Content-Disposition": "inline",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'none'",
        "X-Content-Security-Policy": "default-src 'none'",
        "X-WebKit-CSP": "default-src 'none'",
      }

      return FileResponse(s3_response["Body"], status=status.HTTP_200_OK, headers= headers, content_type=CONTENT_TYPE)
   
      

   def isvalid_token(self, version, auth_token, request, file_path):
      # Validate file sent by the user with auth_token
      file_type = request.META.get('CONTENT_TYPE', '')
      file_size = request.META.get('CONTENT_LENGTH', 0)
      token_string = ''

      if version == "v":
        token_string = bytearray(f'{file_path} {file_size}', 'utf-8')
      else:
        token_string = bytearray(f'{file_path}\x00{file_size}\x00{file_type}', 'utf-8')
      
      token = hmac.new(str.encode(XMPP_UPLOAD_KEY), token_string, hashlib.sha256).hexdigest()
      if token != auth_token:
        return False
      return True
 
   
   def put(self, request, path, filename , format=None):
      file_obj = request.data['file']
      if "v2" not in request.query_params and "v" not in request.query_params:
        return Response({
           "status": "fail",
           "message": "Missing upload service version param 'v' or 'v2'"
        }, status=status.HTTP_403_FORBIDDEN)
      
      version = "v" if "v" in request.query_params else "v2"
      auth_token = request.query_params.get(version)
      file_path = f'{path}/{filename}'
      if not self.isvalid_token(version, auth_token, request, file_path):
        return Response({
           "status": "fail",
           "message": "You send the file that is not conformed with previous declared slot"
        }, status=status.HTTP_403_FORBIDDEN)

      try:
          s3_client.upload_fileobj(file_obj, S3_BUCKET, f'langchat/{file_path}')
      except ClientError as e:
          return Response({
             "status": "fail",
             "message": e
          }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

      return Response(status=status.HTTP_201_CREATED)
   
   def head(self, request, path, filename, format=None):
      try:
        s3_response = s3_client.get_object(Bucket=S3_BUCKET, Key=f'langchat/{path}/{filename}')
      except s3_client.exceptions.NoSuchKey:
        return Response({
           "status": "fail",
           "message": "There is no file having such path"
        }, status=status.HTTP_400_BAD_REQUEST)
      except s3_client.exceptions.InvalidObjectState as e:
         return Response({
           "status": "fail",
           "message": f"{e}"
        }, status=status.HTTP_400_BAD_REQUEST)
      
      headers = {
        "Last-Modified": s3_response['LastModified'],
        "Content-Length": s3_response['ContentLength'],
        "ETag": s3_response['ETag'],
        "Cache-Control": s3_response.get('CacheControl', ''),
        "Content-Disposition": "inline",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'none'",
        "X-Content-Security-Policy": "default-src 'none'",
        "X-WebKit-CSP": "default-src 'none'",
      }

      """
      The content Content-Type may  be different to the file format
      as indicated in extension of the url by the user.
      """
      return Response({
         "status": "success",
      }, status=status.HTTP_200_OK, headers= headers)