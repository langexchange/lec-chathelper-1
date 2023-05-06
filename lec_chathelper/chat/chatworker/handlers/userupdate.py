from chat.models.langchat import Vcard
import json
import logging
from lxml import etree
from django.utils import timezone

logger = logging.getLogger(__name__)

class UserUpdateHandler:
    
    vcardElMapping = {
          "fullname": "FN",
          "nickname": "NICKNAME",
          "avatar_url": "PHOTO EXTVAL",
          "jid": "JABBERID",
        }
    vcardns = 'vcard-temp'
    vcard_el = 'vCard'
    

    def __init__(self):
      pass
        
    """
      {
        "jid": "user_id1@localhost",
        "fullname": "",
        "nickname": "",
        "avatar_url": "",
      },
    """
    def createVcard(data: str) -> str:
      root = etree.Element(UserUpdateHandler.vcard_el, xmlns=UserUpdateHandler.vcardns)

      for field in data:
        if field not in UserUpdateHandler.vcardElMapping:
          logger.warning("Field {} is supported to add in chat app", field)
          continue
        
        cur_element = root
        for element in UserUpdateHandler.vcardElMapping[field].split(" "):
          cur_element = etree.SubElement(cur_element, element)
        cur_element.text = data[field]
    
      return etree.tostring(root, encoding='unicode')
    
    def updateVcard(ovcard, data):
      root = etree.fromstring(ovcard)

      for field in data:
        if field not in UserUpdateHandler.vcardElMapping:
          logger.warning("Field {} is supported to update in chat app", field)
          continue
        
        if field == "jid":
          continue
        
        update_el_tag = "{{{}}}{}".format(UserUpdateHandler.vcardns, UserUpdateHandler.vcardElMapping[field].replace(" ", "/"))
        update_el = root.find(update_el_tag)
        if update_el is None:
          cur_element = root
          for element in UserUpdateHandler.vcardElMapping[field].split(" "):
            cur_element = etree.SubElement(cur_element, element)
          cur_element.text = data[field]
          continue

        update_el.text = data[field]

      return etree.tostring(root, encoding='unicode')

    def handle(msg):
      logger.debug("Message %s is received by %s", msg.value(),  UserUpdateHandler.__name__)
      try:
        data = json.loads(msg.value())
      except ValueError:
        logging.exception("Message received from %s fail to be parsed by %s", msg.topic(), UserUpdateHandler.__name__)
        return
      
      logger.debug("Message %s is received by %s out of json load", msg.value(),  UserUpdateHandler.__name__)

      if "jid" not in data or len(data) == 1:
         logger.warning("Json received does not contain user jid or there is no field to up date")
         return 
      
      user_name = data["jid"].split("@")[0]
      user_filters =  Vcard.objects.filter(username=user_name)
      if not user_filters:
        # We create a new user
        vcard = UserUpdateHandler.createVcard(data)
        user_vcard = Vcard(username = user_name, vcard = vcard)
        user_vcard.save()
        logger.debug("Vcard %s added for user %s", vcard,  user_name)
        return
      
      user_vcard = user_filters[0]
      update_vcard = UserUpdateHandler.updateVcard(user_vcard.vcard, data)
      user_vcard.vcard = update_vcard
      user_vcard.save()
      logger.debug("Vcard %s updated from data %s for user %s", update_vcard, data, user_name)

      return
        