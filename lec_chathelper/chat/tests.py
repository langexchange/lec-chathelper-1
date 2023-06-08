# from django.test import TestCase
# from .models.langchat import Rosterusers
# # Create your tests here.

# class ChatTestCase(TestCase):
#   def setUp(self):
#     Rosterusers.objects.filter().delete

#   def test_duplicate(self):
#     user_name = "vutl"
#     jid = "hello@localhost"
    
#     # Add user vutl first
#     user = Rosterusers(username=user_name, jid=jid, type="item", subscription="B")
#     user.save()

#     # Test if I can update thorugh update_or_create
#     _, iscreate = Rosterusers.objects.update_or_create(username = user_name, jid= jid, defaults={"type": "item", "subscription": "B" if "friend" == "friend" else "N"})

#     self.assertEqual(iscreate, False)


