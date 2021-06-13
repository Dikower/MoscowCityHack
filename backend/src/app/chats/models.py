from enum import Enum
from tortoise import Model, Tortoise, fields


class ChatType(str, Enum):
    PRIVATE = "PRIVATE"
    GROUP = "GROUP"
    CHANNEL = "CHANNEL"


class Chat(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=128)
    type: ChatType = fields.CharEnumField(ChatType, default=ChatType.PRIVATE)
    members = fields.ManyToManyField('users.User', related_name='chats')
    admins = fields.ManyToManyField('users.ChatAdmin', related_name='chats')
    # messages: fields.ForeignKeyRelation['chats.Message']


class Message(Model):
    id = fields.UUIDField(pk=True)
    sender = fields.ForeignKeyField('users.User')
    chat = fields.ForeignKeyField('chats.Chat', related_name='messages')
    text = fields.CharField(max_length=1024)
    time = fields.DatetimeField(auto_now=True)
    # TODO attachments


Tortoise.init_models(["app.chats.models"], "chats")
