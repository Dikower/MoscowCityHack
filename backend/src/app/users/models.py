from enum import Enum
from tortoise import Model, Tortoise, fields


class UserType(str, Enum):
    BOT = "BOT"
    PERSON = "PERSON"
    ADMIN = "ADMIN"


class User(Model):
    id = fields.UUIDField(pk=True)
    fio = fields.CharField(null=True, max_length=128)
    email = fields.CharField(unique=True, max_length=512)
    auth_token = fields.CharField(null=True, max_length=1024)
    avatar = fields.CharField(null=True, max_length=512)
    type: UserType = fields.CharEnumField(UserType, default=UserType.PERSON)

    as_chat_admin: fields.ForeignKeyRelation['users.ChatAdmin']
    chats: fields.ForeignKeyRelation['chats.Chat']

    def __repr__(self):
        return str(self.fio)

    class PydanticMeta:
        exclude = ["hashed_password"]


class ChatAdmin(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('users.User', related_name='as_chat_admin')
    chats: fields.ForeignKeyRelation['chats.Chat']


class Token(Model):
    id = fields.IntField(pk=True)
    login_token = fields.CharField(max_length=2048)
    is_used = fields.BooleanField(default=False)


