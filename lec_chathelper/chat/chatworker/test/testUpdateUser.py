from django.test import TestCase
from django.urls import reverse
from chat.models.langchat import Vcard
from ..handlers.userupdate import UserUpdateHandler
from unittest.mock import MagicMock
from lxml import etree

class UserUpdateTestCase(TestCase):
    # def setUp(self):
    #     # Set up any initial data or objects required for the tests
    #     YourModel.objects.create(name="Test Model", description="Test Description")

    def test_update_url(self):
        # Retrieve the object from the database
        # Mock an msg.value() objects here
        msg = MagicMock()
        msg.value.return_value = b"""
        {  
          "jid":"3dbe7b0a-ffef-46fe-9157-0c93d463484b@localhost",
          "avatar_url":"https://language-exchanged.s3.ap-southeast-1.amazonaws.com/image/000/000/028/20230607093509/Jennie.jpg",
          "is_created":false,"target_langs":[],
          "MessageId":"f1c228f2-9eb1-41ad-807d-9f98e9af3a3d",
          "MessageName":"chathelper-userinfo",
          "CreatedAt":"2023-06-07T09:35:13.3231803Z"
        }
        """

        
        msg.topic.return_value = "update_topic"
        # FIXME: ERROR current transaction is aborted, commands ignored until end of transaction block
        UserUpdateHandler.handle(msg)

        # Extract avatar_url element
        user_vcard =  Vcard.objects.filter(username="3dbe7b0a-ffef-46fe-9157-0c93d463484b")
        root = etree.fromstring(user_vcard[0].vcard)
        avatar_url_tag = "{{{}}}{}".format(UserUpdateHandler.vcardns, UserUpdateHandler.vcardElMapping["avatar_url"].replace(" ", "/"+ "{%s}" % UserUpdateHandler.vcardns))
        avatar_url_el = root.find(avatar_url_tag)

        self.assertEqual(avatar_url_el.text, "https://language-exchanged.s3.ap-southeast-1.amazonaws.com/image/000/000/028/20230607093509/Jennie.jpg")