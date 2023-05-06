from chat.models.langchat import Rosterusers
import json
import logging

logger = logging.getLogger(__name__)

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
      
      user1_name = data["jid1"].split("@")[0]
      user2_name = data["jid2"].split("@")[0]

      # We filter and update instead of using save as Django does not provide save() method for composite key

      user_contact =  Rosterusers.objects.filter(username = user1_name, jid=data["jid2"])  

      if not user_contact:
        user_contact1 = Rosterusers(username = user1_name, jid=data["jid2"], type= "item", subscription= "B" if data["state"] == "friend" else "N")
        user_contact2 = Rosterusers(username = user2_name, jid=data["jid1"], type= "item", subscription= "B" if data["state"] == "friend" else "N")
        user_contact1.save()
        user_contact2.save()
        logger.debug("New contacts is added to 2 user's roster %s %s", user1_name, user2_name)
        return
      
      
      try: 
        logger.debug("Update rosteruser table...")
        Rosterusers.objects.filter(username = user1_name, jid=data["jid2"]).update(type= "item", subscription= "B" if data["state"] == "friend" else "N")

        Rosterusers.objects.filter(username = user2_name, jid=data["jid1"]).update(type= "item", subscription= "B" if data["state"] == "friend" else "N")
      except Exception as e:
        logger.exception("Fail to update record %s %s", msg.topic(), type(e))
        raise('Fail to update record {}'.format(msg.topic()))

      logger.info("Message %s is  successfully processed by %s", msg.value(),  FriendStateHandler.__name__)
        