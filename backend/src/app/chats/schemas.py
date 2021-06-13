from .models import Chat
from tortoise.contrib.pydantic import pydantic_model_creator

Preview = pydantic_model_creator(Chat, exclude=('messages', ))
