from tortoise import Tortoise
Tortoise.init_models(['app.users.models'], 'users')  # <- added
