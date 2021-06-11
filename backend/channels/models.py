from tortoise.models import Model
from tortoise import fields


class Channel(Model):
    id = fields.IntField(pk=True)
    subs = fields.ManyToManyField('users.User')
