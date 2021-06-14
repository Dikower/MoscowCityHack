from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel

from ..auth_helpers import generate_auth_token, get_user_data_by_auth_token
from ..users.models import User


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class BotData(BaseModel):
    name: str


class BotMessage(BaseModel):
    bot_id: str
    chat_id: str
    message: str


@router.post("/create_bot")
async def create_bot(bot_data: BotData, auth_token=Depends(oauth2_scheme)):
    try:
        await get_user_data_by_auth_token(auth_token)
    except jwt.JWTError:
        raise credentials_exception

    bot_id = uuid4()

    await User.create(id=bot_id, fio=bot_data.name, type="BOT")

    return bot_id


@router.post("/send_message")
async def send_message(bot_message: BotMessage, auth_token=Depends(oauth2_scheme)):
    try:
        await get_user_data_by_auth_token(auth_token)
    except jwt.JWTError:
        raise credentials_exception

    # TODO send message

    return "TODO"
