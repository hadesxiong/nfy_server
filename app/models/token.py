# coding=utf8
from tortoise import fields
from tortoise.models import Model

class TokenMain(Model):

    usr_id = fields.CharField(max_length=32,unqiue=True)
    usr_aid = fields.CharField(max_length=128,unique=True)
    usr_secret = fields.CharField(max_length=128,unique=True)
    secret_update_dt = fields.DatetimeField(null=True,auto_now_add=True)

    class Meta:
        table = 'nfy_token_main'