from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone
import uuid

class LangChatModels:
    models = ["ChatUsers", "Rosterusers"]
    db_name = "default"

class ChatUsers(models.Model):
    username = models.TextField(primary_key=True)
    password = models.TextField()
    serverkey = models.TextField()
    salt = models.TextField()
    iterationcount = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        managed = False
        # db_table = 'chatusers'
        db_table = 'users'
        

class Rosterusers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.TextField()
    jid = models.TextField()
    nick = models.TextField()
    subscription = models.CharField(max_length=1)
    ask = models.CharField(max_length=1)
    askmessage = models.TextField()
    server = models.CharField(max_length=1)
    subscribe = models.TextField()
    type = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'rosterusers'

class Vcard(models.Model):
    username = models.TextField(primary_key=True)
    vcard = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'vcard'
    
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# class Archive(models.Model):
#     username = models.TextField()
#     timestamp = models.BigIntegerField()
#     peer = models.TextField()
#     bare_peer = models.TextField()
#     xml = models.TextField()
#     txt = models.TextField(blank=True, null=True)
#     id = models.BigAutoField()
#     kind = models.TextField(blank=True, null=True)
#     nick = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'archive'


# class ArchivePrefs(models.Model):
#     username = models.TextField(primary_key=True)
#     def_field = models.TextField(db_column='def')  # Field renamed because it was a Python reserved word.
#     always = models.TextField()
#     never = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'archive_prefs'


# class Bosh(models.Model):
#     sid = models.TextField(unique=True)
#     node = models.TextField()
#     pid = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'bosh'


# class CapsFeatures(models.Model):
#     node = models.TextField()
#     subnode = models.TextField()
#     feature = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'caps_features'


# class FlywaySchemaHistory(models.Model):
#     installed_rank = models.IntegerField(primary_key=True)
#     version = models.CharField(max_length=50, blank=True, null=True)
#     description = models.CharField(max_length=200)
#     type = models.CharField(max_length=20)
#     script = models.CharField(max_length=1000)
#     checksum = models.IntegerField(blank=True, null=True)
#     installed_by = models.CharField(max_length=100)
#     installed_on = models.DateTimeField()
#     execution_time = models.IntegerField()
#     success = models.BooleanField()

#     class Meta:
#         managed = False
#         db_table = 'flyway_schema_history'


# class Last(models.Model):
#     username = models.TextField(primary_key=True)
#     seconds = models.TextField()
#     state = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'last'


# class MixChannel(models.Model):
#     channel = models.TextField()
#     service = models.TextField()
#     username = models.TextField()
#     domain = models.TextField()
#     jid = models.TextField()
#     hidden = models.BooleanField()
#     hmac_key = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'mix_channel'
#         unique_together = (('channel', 'service'),)


# class MixPam(models.Model):
#     username = models.TextField()
#     channel = models.TextField()
#     service = models.TextField()
#     id = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'mix_pam'
#         unique_together = (('username', 'channel', 'service'),)


# class MixParticipant(models.Model):
#     channel = models.TextField()
#     service = models.TextField()
#     username = models.TextField()
#     domain = models.TextField()
#     jid = models.TextField()
#     id = models.TextField()
#     nick = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'mix_participant'
#         unique_together = (('channel', 'service', 'username', 'domain'),)


# class MixSubscription(models.Model):
#     channel = models.TextField()
#     service = models.TextField()
#     username = models.TextField()
#     domain = models.TextField()
#     node = models.TextField()
#     jid = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'mix_subscription'
#         unique_together = (('channel', 'service', 'username', 'domain', 'node'),)


# class Motd(models.Model):
#     username = models.TextField(primary_key=True)
#     xml = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'motd'


# class MqttPub(models.Model):
#     username = models.TextField()
#     resource = models.TextField()
#     topic = models.TextField(unique=True)
#     qos = models.SmallIntegerField()
#     payload = models.BinaryField()
#     payload_format = models.SmallIntegerField()
#     content_type = models.TextField()
#     response_topic = models.TextField()
#     correlation_data = models.BinaryField()
#     user_properties = models.BinaryField()
#     expiry = models.BigIntegerField()

#     class Meta:
#         managed = False
#         db_table = 'mqtt_pub'


# class MucOnlineRoom(models.Model):
#     name = models.TextField()
#     host = models.TextField()
#     node = models.TextField()
#     pid = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'muc_online_room'
#         unique_together = (('name', 'host'),)


# class MucOnlineUsers(models.Model):
#     username = models.TextField()
#     server = models.TextField()
#     resource = models.TextField()
#     name = models.TextField()
#     host = models.TextField()
#     node = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'muc_online_users'
#         unique_together = (('username', 'server', 'resource', 'name', 'host'),)


# class MucRegistered(models.Model):
#     jid = models.TextField()
#     host = models.TextField()
#     nick = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'muc_registered'
#         unique_together = (('jid', 'host'),)


# class MucRoom(models.Model):
#     name = models.TextField()
#     host = models.TextField()
#     opts = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'muc_room'
#         unique_together = (('name', 'host'),)


# class MucRoomSubscribers(models.Model):
#     room = models.TextField()
#     host = models.TextField()
#     jid = models.TextField()
#     nick = models.TextField()
#     nodes = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'muc_room_subscribers'
#         unique_together = (('host', 'room', 'jid'),)


# class OauthClient(models.Model):
#     client_id = models.TextField(primary_key=True)
#     client_name = models.TextField()
#     grant_type = models.TextField()
#     options = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'oauth_client'


# class OauthToken(models.Model):
#     token = models.TextField(unique=True)
#     jid = models.TextField()
#     scope = models.TextField()
#     expire = models.BigIntegerField()

#     class Meta:
#         managed = False
#         db_table = 'oauth_token'


# class PrivacyDefaultList(models.Model):
#     username = models.TextField(primary_key=True)
#     name = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'privacy_default_list'


# class PrivacyList(models.Model):
#     username = models.TextField()
#     name = models.TextField()
#     id = models.BigAutoField(unique=True)
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'privacy_list'
#         unique_together = (('username', 'name'),)


# class PrivacyListData(models.Model):
#     id = models.ForeignKey(PrivacyList, models.DO_NOTHING, db_column='id', blank=True, null=True)
#     t = models.CharField(max_length=1)
#     value = models.TextField()
#     action = models.CharField(max_length=1)
#     ord = models.DecimalField(max_digits=65535, decimal_places=65535)
#     match_all = models.BooleanField()
#     match_iq = models.BooleanField()
#     match_message = models.BooleanField()
#     match_presence_in = models.BooleanField()
#     match_presence_out = models.BooleanField()

#     class Meta:
#         managed = False
#         db_table = 'privacy_list_data'


# class PrivateStorage(models.Model):
#     username = models.TextField()
#     namespace = models.TextField()
#     data = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'private_storage'
#         unique_together = (('username', 'namespace'),)


# class Proxy65(models.Model):
#     sid = models.TextField(unique=True)
#     pid_t = models.TextField()
#     pid_i = models.TextField()
#     node_t = models.TextField()
#     node_i = models.TextField()
#     jid_i = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'proxy65'


# class PubsubItem(models.Model):
#     nodeid = models.ForeignKey('PubsubNode', models.DO_NOTHING, db_column='nodeid', blank=True, null=True)
#     itemid = models.TextField()
#     publisher = models.TextField()
#     creation = models.CharField(max_length=32)
#     modification = models.CharField(max_length=32)
#     payload = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'pubsub_item'
#         unique_together = (('nodeid', 'itemid'),)


# class PubsubNode(models.Model):
#     host = models.TextField()
#     node = models.TextField()
#     parent = models.TextField()
#     plugin = models.TextField()
#     nodeid = models.BigAutoField(unique=True)

#     class Meta:
#         managed = False
#         db_table = 'pubsub_node'
#         unique_together = (('host', 'node'),)


# class PubsubNodeOption(models.Model):
#     nodeid = models.ForeignKey(PubsubNode, models.DO_NOTHING, db_column='nodeid', blank=True, null=True)
#     name = models.TextField()
#     val = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'pubsub_node_option'


# class PubsubNodeOwner(models.Model):
#     nodeid = models.ForeignKey(PubsubNode, models.DO_NOTHING, db_column='nodeid', blank=True, null=True)
#     owner = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'pubsub_node_owner'


# class PubsubState(models.Model):
#     nodeid = models.ForeignKey(PubsubNode, models.DO_NOTHING, db_column='nodeid', blank=True, null=True)
#     jid = models.TextField()
#     affiliation = models.CharField(max_length=1, blank=True, null=True)
#     subscriptions = models.TextField()
#     stateid = models.BigAutoField(unique=True)

#     class Meta:
#         managed = False
#         db_table = 'pubsub_state'
#         unique_together = (('nodeid', 'jid'),)


# class PubsubSubscriptionOpt(models.Model):
#     subid = models.TextField()
#     opt_name = models.CharField(max_length=32, blank=True, null=True)
#     opt_value = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'pubsub_subscription_opt'
#         unique_together = (('subid', 'opt_name'),)


# class PushSession(models.Model):
#     username = models.TextField()
#     timestamp = models.BigIntegerField()
#     service = models.TextField()
#     node = models.TextField()
#     xml = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'push_session'
#         unique_together = (('username', 'service', 'node'),)


# class RosterVersion(models.Model):
#     username = models.TextField(primary_key=True)
#     version = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'roster_version'


# class Rostergroups(models.Model):
#     username = models.TextField()
#     jid = models.TextField()
#     grp = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'rostergroups'


# class Rosterusers(models.Model):
#     username = models.TextField()
#     jid = models.TextField()
#     nick = models.TextField()
#     subscription = models.CharField(max_length=1)
#     ask = models.CharField(max_length=1)
#     askmessage = models.TextField()
#     server = models.CharField(max_length=1)
#     subscribe = models.TextField()
#     type = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'rosterusers'
#         unique_together = (('username', 'jid'),)


# class Route(models.Model):
#     domain = models.TextField()
#     server_host = models.TextField()
#     node = models.TextField()
#     pid = models.TextField()
#     local_hint = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'route'
#         unique_together = (('domain', 'server_host', 'node', 'pid'),)


# class Sm(models.Model):
#     usec = models.BigIntegerField()
#     pid = models.TextField()
#     node = models.TextField()
#     username = models.TextField()
#     resource = models.TextField()
#     priority = models.TextField()
#     info = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'sm'
#         unique_together = (('usec', 'pid'),)


# class Spool(models.Model):
#     username = models.TextField()
#     xml = models.TextField()
#     seq = models.BigAutoField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'spool'


# class SrGroup(models.Model):
#     name = models.TextField(unique=True)
#     opts = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'sr_group'


# class SrUser(models.Model):
#     jid = models.TextField()
#     grp = models.TextField()
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'sr_user'
#         unique_together = (('jid', 'grp'),)




# class VcardSearch(models.Model):
#     username = models.TextField()
#     lusername = models.TextField(primary_key=True)
#     fn = models.TextField()
#     lfn = models.TextField()
#     family = models.TextField()
#     lfamily = models.TextField()
#     given = models.TextField()
#     lgiven = models.TextField()
#     middle = models.TextField()
#     lmiddle = models.TextField()
#     nickname = models.TextField()
#     lnickname = models.TextField()
#     bday = models.TextField()
#     lbday = models.TextField()
#     ctry = models.TextField()
#     lctry = models.TextField()
#     locality = models.TextField()
#     llocality = models.TextField()
#     email = models.TextField()
#     lemail = models.TextField()
#     orgname = models.TextField()
#     lorgname = models.TextField()
#     orgunit = models.TextField()
#     lorgunit = models.TextField()

#     class Meta:
#         managed = False
#         db_table = 'vcard_search'
