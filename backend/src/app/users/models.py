from enum import unique
from tortoise import Model, Tortoise, fields


class User(Model):
    id = fields.UUIDField(pk=True, generated=False)
    fio = fields.CharField(null=True, max_length=128)
    email = fields.CharField(unique=True, max_length=512)
    auth_token = fields.CharField(null=True, max_length=1024)
    avatar = fields.CharField(null=True, max_length=512)

    # channels: fields.ManyToManyRelation['channels.Channel']
    # bots: fields.ManyToManyRelation['bots.Bot']

    def __repr__(self):
        return str(self.fio)

    class PydanticMeta:
        exclude = ["hashed_password"]


class Token(Model):
    id = fields.IntField(pk=True)
    login_token = fields.CharField(max_length=2048)
    is_used = fields.BooleanField(default=False)
