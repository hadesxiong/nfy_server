# coding=utf8
from tortoise import fields
from tortoise.models import Model

class UserAuth(Model):

    usr_id = fields.CharField(max_length=32,unique=True)
    usr_name = fields.CharField(max_length=64)
    usr_pwd = fields.CharField(max_length=255)
    auth_update_dt = fields.DatetimeField(null=True,auto_now_add=True)
    auth_ext_data = fields.JSONField()

    class Meta:
        table = 'nfy_pwd_auth'

class UserMain(Model):

    usr_id = fields.CharField(max_length=32,unique=True)
    usr_name = fields.CharField(max_length=64)
    usr_avatar = fields.TextField(null=True)
    usr_role = fields.IntField(default=1)
    usr_stu = fields.IntField(default=1)
    usr_auth_type = fields.IntField(null=False)
    usr_create_dt = fields.DatetimeField(null=True,auto_now_add=True)
    usr_ext_data = fields.JSONField(null=True)

    class Meta:
        table = 'nfy_usr_main'

class DictMark(Model):

    mark_id = fields.CharField(max_length=32,unique=True)
    mark_index = fields.CharField(max_length=128)
    mark_code = fields.IntField()
    mark_value = fields.CharField(max_length=128)
    marK_stu = fields.IntField()
    mark_abbr = fields.CharField(max_length=128)
    mark_ext_data = fields.JSONField()

    class Meta:
        table = 'nfy_dict_mark'