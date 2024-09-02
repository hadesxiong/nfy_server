# coding=utf8
from tortoise import fields
from tortoise.models import Model

class NfyChnl(Model):

    chnl_id = fields.CharField(max_length=32,unique=True)
    chnl_name = fields.CharField(max_length=128)
    chnl_type = fields.IntField(default=1)
    chnl_stu = fields.IntField(default=1)
    chnl_host = fields.CharField(max_length=255)
    chnl_auth_method = fields.IntField(default=1)
    chnl_auth_data = fields.JSONField(null=True)
    chnl_create_usr = fields.CharField(max_length=32)
    chnl_create_dt = fields.DatetimeField(null=True,auto_now_add=True)
    chnl_update_usr = fields.CharField(max_length=32)
    chnl_update_dt = fields.DatetimeField(null=True,auto_now_add=True)
    chnl_ext_data = fields.JSONField(null=True)

    class Meta:
        table = 'nfy_chnl_main'

class NfyTmpl(Model):

    tmpl_id = fields.CharField(max_length=32,unique=True)
    tmpl_chnl = fields.CharField(max_length=32)
    tmpl_title = fields.CharField(max_length=255)
    tmpl_stu = fields.IntField(default=1)
    tmpl_args = fields.JSONField(null=True)
    tmpl_create_usr = fields.CharField(max_length=32)
    tmpl_create_dt = fields.DatetimeField(null=True,auto_now_add=True)
    tmpl_update_usr = fields.CharField(max_length=32)
    tmpl_update_dt = fields.DatetimeField(null=True,auto_now_add=True)
    tmpl_ext_data = fields.JSONField(null=True)

    class Meta:
        table = 'nfy_tmpl_main'

class NfyRec(Model):

    rec_id = fields.CharField(max_length=32,unique=True)
    tmpl_id = fields.CharField(max_length=32)
    rec_use = fields.CharField(max_length=64)
    call_from = fields.CharField(max_length=128)
    rec_data = fields.JSONField(null=True)
    rec_code = fields.IntField()
    rec_res = fields.CharField(max_length=12)
    rec_msg = fields.TextField()
    rec_rcv = fields.CharField(max_length=32)
    rec_batch = fields.CharField(max_length=64)
    rec_ext_data = fields.JSONField(null=True)

    class Meta:
        table = 'nfy_rec_main'