from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from .models import User


PublicUser = pydantic_model_creator(
    User, name='PublicUser', exclude=(), include=()
)
