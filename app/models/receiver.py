# conding=utf8
from tortoise import fields
from tortoise.models import Model

class RcvMain(Model):

    rcv_id = fields.CharField(max_length=32,unique=True)
    rcv_chnl = fields.CharField(max_length=128)
    rcv_stu = fields.IntField(default=1)
    rcv_type = fields.IntField(default=1)
    rcv_create_dt = fields.DatetimeField(null=True,auto_now_add=True)
    rcv_create_usr = fields.CharField(max_length=32)
    rcv_update_dt = fields.DatetimeField(null=True,auto_now_add=True)
    rcv_update_usr = fields.CharField(max_length=32)
    rcv_ext_data = fields.JSONField(null=True)

    class Meta:
        table = 'nfy_rcv_main'

class RcvBark(Model):

    rcv_id = fields.CharField(max_length=32,unique=True)
    device_key = fields.CharField(max_length=128)
    rcv_key = fields.CharField(max_length=128)
    rcv_iv = fields.CharField(max_length=128)
    bark_ext_data = fields.JSONField(null=True)

    class Meta:
        table = 'nfy_rcv_bark'

class RcvNtfy(Model):

    rcv_id = fields.CharField(max_length=32,unique=True)
    rcv_name = fields.CharField(max_length=128)
    rcv_role = fields.IntField(default=1)
    rcv_topic = fields.CharField(max_length=255)
    rcv_perm = fields.IntField(default=1)
    ntfy_ext_data = fields.JSONField(null=True)

    class Meta:
        table = 'nfy_rcv_ntfy'

class RcvGroup(Model):

    group_id = fields.CharField(max_length=32,unique=True)
    group_name = fields.CharField(max_length=128)
    group_type = fields.IntField(default=1)
    group_stu = fields.IntField(default=1)
    group_rcv = fields.JSONField(null=True)
    group_create_usr = fields.CharField(max_length=64)
    group_update_usr = fields.CharField(max_length=64)
    group_create_dt = fields.DatetimeField(null=True,auto_now_add=True)
    group_update_dt = fields.DatetimeField(null=True,auto_now_add=True)
    group_ext_data = fields.JSONField(null=True)

    class Meta:
        table = 'nfy_rcv_group'