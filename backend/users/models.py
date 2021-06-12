from tortoise import Model, Tortoise, fields


class User(Model):
    id = fields.IntField(pk=True)
    fio = fields.CharField(null=True, max_length=128)
    auth_token  = fields.CharField(null=True, max_length=1024)

    channels: fields.ManyToManyRelation['channels.Channel']
    bots: fields.ManyToManyRelation['bots.Bot']

    def __repr__(self):
        return str(self.fio)

    class PydanticMeta:
        exclude = ['hashed_password']
