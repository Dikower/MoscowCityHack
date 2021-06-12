from tortoise import Model, Tortoise, fields


class Chat(Model):
    id = fields.IntField(pk=True)

