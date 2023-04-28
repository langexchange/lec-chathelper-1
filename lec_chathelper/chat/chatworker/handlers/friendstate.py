from chat.models.langchat import Rosterusers
import json
import logging

logger = logging.getLogger(__name__)

class FriendStateHandler:
    def __init__(self):
        pass
    
    """
      {
        "jid1": "vutl@localhost",
        "jid2": "hello@localhost",
        "state": "friend"
      },

      {
        "jid1": "vutl@localhost",
        "jid2": "thuongnguyen@localhost",
        "state": "friend"
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
      try: 
        logger.debug("Update rosteruser table...")
        Rosterusers.objects.filter(username = user1_name, jid=data["jid2"]).update(type= "item", subscription= "B" if data["state"] == "friend" else "N")

        Rosterusers.objects.filter(username = user2_name, jid=data["jid1"]).update(type= "item", subscription= "B" if data["state"] == "friend" else "N")
      except Exception as e:
        logger.exception("Fail to update record %s %s", msg.topic(), type(e))
        raise('Fail to update record {}'.format(msg.topic()))
      finally:
        logger.debug("Some error encountered here !!!")

      logger.info("Message %s is  successfully processed by %s", msg.value(),  FriendStateHandler.__name__)
        