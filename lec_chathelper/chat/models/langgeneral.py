from django.db import models
import uuid
db_name = "langgeneral"

class LangGeneralModels:
    models = ["Language", "Users", "Notibox"]
    db_name = "langgeneral"

class Language(models.Model):
    langid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, blank=True, null=True)
    locale_code = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        app_label = "chat"
        db_table = 'language'

class Notibox(models.Model):
    boxid = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        app_label = "chat"
        db_table = 'notibox'


class Users(models.Model):
    userid = models.UUIDField(primary_key=True)
    longtt = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latt = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    native_lang = models.ForeignKey(Language, models.DO_NOTHING, db_column='native_lang', blank=True, null=True)
    notibox = models.ForeignKey(Notibox, models.DO_NOTHING, db_column='notibox', blank=True, null=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    middle_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    gender = models.CharField(max_length=5, blank=True, null=True)
    introduction = models.CharField(max_length=1024, blank=True, null=True)
    native_level = models.IntegerField(blank=True, null=True)
    is_tutor = models.BooleanField(blank=True, null=True)
    is_restrict = models.BooleanField(blank=True, null=True)
    is_removed = models.BooleanField(blank=True, null=True)
    temp_token = models.CharField(max_length=128, blank=True, null=True)
    token_iat = models.DateTimeField(blank=True, null=True)
    # user_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        app_label = "chat"
        managed = False
        db_table = 'users'