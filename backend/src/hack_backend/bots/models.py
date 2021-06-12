from tortoise import Model, Tortoise, fields


class Bot(Model):
    id = fields.IntField(pk=True)
    users = fields.ManyToManyField('users.User', related_name='bots')

