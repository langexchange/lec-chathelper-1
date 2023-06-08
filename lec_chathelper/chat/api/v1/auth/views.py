from django.http import JsonResponse, HttpResponseBadRequest
import jwt
import os
import environ
import time
from chat.models.langgeneral import Users
from lec_chathelper.settings import BASE_DIR
# Token ASE decrypt
from base64 import b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import  unpad


## Read environment variables
env = environ.Env()
# TODO: Modify this using sys.path
environ.Env.read_env(os.path.join(BASE_DIR,'env/.dev.env'))

### GLOBAL VARIABLE
jwt_secret = env('CREDENTIALS_KEY')
host = env('HOST')
token_db_key = env('TOKEN_DB_KEY')
iv = env('IV')


def get_credentials(request):
    try:
      token = request.GET.__getitem__('token')
    except KeyError:
      return HttpResponseBadRequest('Lack of token in parameter')
    
    # Parsing token
    # try:
    #   payload = jwt.decode(token, jwt_secret, algorithms=["HS256"],options={
    #     "require":["iat", "exp"],
    #   })
    # except jwt.exceptions.DecodeError:
    #   return HttpResponseBadRequest('Invalid url')
    # except jwt.exceptions.ExpiredSignatureError:
    #   return HttpResponseBadRequest('Expired url')
    # except jwt.exceptions.ImmatureSignatureError:
    #   return HttpResponseBadRequest('Iat time is in the future')
    # except:
    #   return HttpResponseBadRequest('Missing field in token iat or exp')
    
    # # Get user name
    # if "uid" not in payload:
    #   return HttpResponseBadRequest('Token does not contain user name')
    
    # uid = payload["uid"]

    # #Check if the url is old
    # try:
    #   user = Users.objects.filter(userid=uid).values('email' ,'token_iat', 'temp_token')[0]
    # except Users.DoesNotExist:
    #   return HttpResponseBadRequest('The user does not exist')
    # except Users.MultipleObjectsReturned as e: 
    #   return HttpResponseBadRequest(str(e))
    # # except:
    # #   return HttpResponseBadRequest('Error happend at get_credentials after user = Users.objects.filter(userid=uid).values')
    # # except:
    # #   return HttpResponseBadRequest("Error does not know at get_credentials")
    
    # if "token_iat" not in user or "temp_token" not in user:
    #   return HttpResponseBadRequest("The user has not logined in before")

    # # Check if it is old url
    # mrecent_epoch_ita = time.mktime(user["token_iat"].timetuple())

    # if payload["iat"] < mrecent_epoch_ita:
    #   return HttpResponseBadRequest('Old url')
    
    # # Get token from encrypted text
    # try:
    #   cipher = AES.new(token_db_key.encode(), AES.MODE_CBC, iv=iv.encode())
    #   ecrpt_bytetoken = b64decode(user["temp_token"])
    #   token = unpad(cipher.decrypt(ecrpt_bytetoken), AES.block_size).decode()
    # except (ValueError, KeyError):
    #   return HttpResponseBadRequest('System error: Token db key is not matched')

    # user_name = user["email"].split('@')[0]
    # return JsonResponse(data={
    #     "jid" : "{user_name}@{host}".format(user_name=user_name,host=host),
    #     "password": token
    # })