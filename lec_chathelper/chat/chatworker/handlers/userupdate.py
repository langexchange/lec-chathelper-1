from chat.models.langchat import Rosterusers
import json
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

class UserUpdateHandler:
    def __init__(self):
        pass
    
    def handle(msg):
      logger.debug("Message %s is received by %s", msg.value(),  UserUpdateHandler.__name__)
      try:
        data = json.loads(msg.value())
      except ValueError:
        logging.exception("Message received from %s fail to be parsed by %s", msg.topic(), UserUpdateHandler.__name__)
        return
      
      logger.debug("Message %s is received by %s out of json load", msg.value(),  UserUpdateHandler.__name__)

      if "user" not in data or "nickname" not in data:
         logger.warning("Json received does not contain user or nickname field at %s", msg.topic(), UserUpdateHandler.__name__)
         return 
      

      user_name = data["user"].split("@")[0]
      if "jid" in data: #User change jid of their roster friend
        try: 
          Rosterusers.objects.filter(username=user_name, jid=data["jid"]).update(nick = data["nickname"])
        except Exception as e:
          logger.debug("Fail to update record %s %s", msg.topic(), type(e))
          raise('Fail to update record {}'.format(msg.topic()))

        logger.info("User {%s} change nickname of user having {%s} to be %s processed by %s",user_name, data["jid"], data["nickname"] , UserUpdateHandler.__name__)

        return 
      
      # Users change their own jid
      try: 
        Rosterusers.objects.filter(username=data["user"]).update(nick = data["nickname"])
      except Exception as e:
          logger.exception("Fail to update record %s %s", msg.topic(), type(e))
          raise('Fail to update record {}'.format(msg.topic()))
      
      logger.info("User {%s} change her own nickname to be %s processed by %s",user_name, data["nickname"] , UserUpdateHandler.__name__)
        