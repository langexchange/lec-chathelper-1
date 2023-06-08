from chat.models.langchat import Rosterusers
import json
import logging
import environ

logger = logging.getLogger(__name__)

env = environ.Env()
LANGCHAT_HOST = env('LANGCHAT_HOST')


class FriendStateHandler:
    def __init__(self):
        pass
    """
      {
        "jid1": "user_id1@localhost",
        "jid2": "user_id2@localhost",
        "state": "friend"
      },

      {
        "jid1": "user_id1@localhost",
        "jid2": "user_id2@localhost",
        "state": "unfriend"
      },
      
    """

    def addFriendRelationship(user1_name, user2_name):
      user_contact1 = Rosterusers(username = user1_name, jid="{}@{}".format(user2_name, LANGCHAT_HOST), type= "item", subscription= "B")
      user_contact2 = Rosterusers(username = user2_name, jid="{}@{}".format(user1_name, LANGCHAT_HOST), type= "item", subscription= "B")
      user_contact1.save()
      user_contact2.save()
      logger.debug("New contacts is added to 2 user's roster %s %s", user1_name, user2_name)
    

    def removeRelationShip(user1_name, user2_name):
      try:
        Rosterusers.objects.filter(username = user1_name, jid="{}@{}".format(user2_name, LANGCHAT_HOST)).delete()
        Rosterusers.objects.filter(username = user2_name, jid="{}@{}".format(user1_name, LANGCHAT_HOST)).delete()
        logger.debug("Remove relationship between %s %s successfully", user1_name, user2_name)
      except Exception as e:
        logger.exception("Fail to remove relationship between %s %s %s", user1_name, user2_name, e)
        raise("Fail to remove relationship between %s %s %s", user1_name, user2_name, e)
      
      
    def handle(msg):
      logger.debug("Message %s is received by %s", msg.value(),  FriendStateHandler.__name__)
      try:
        data = json.loads(msg.value())
      except ValueError:
        logger.exception("Message received from %s fail to be parsed", msg.topic())
        raise('Decoding JSON has failed')
      
      logger.debug("Message %s is received by %s out of json load", msg.value(),  FriendStateHandler.__name__)
      if "jid1" not in data or "jid2" not in data or "state" not in data:
         return 
      

      # We filter and update instead of using save as Django does not provide save() method for composite key
      user1_name = data["jid1"].split("@")[0]
      user2_name = data["jid2"].split("@")[0]
      user_contact =  Rosterusers.objects.filter(username = user1_name, jid=data["jid2"])  
      if not user_contact and data["state"]=="friend":
        FriendStateHandler.addFriendRelationship(user1_name, user2_name)
        return
      if data["state"]=="unfriend":
        FriendStateHandler.removeRelationShip(user1_name, user2_name)
        return
      logger.warning("We do not update old existing relationship...")