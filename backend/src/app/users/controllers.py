import json
import os
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel

from .core import generate_auth_token, get_user_data_by_auth_token
from .models import User

current_path = os.path.dirname(os.path.realpath(__file__))

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/users/auth")
async def auth(token: str):
    # TODO validate login token
    user = await User.create(id_=uuid4(), fio="Zalupkin A.I")
    auth_token = await generate_auth_token(user.id_)
    await user.update_from_dict({"auth_token": auth_token})
    await user.save()
    return auth_token


@router.post("/users/get_me")
async def get_me(auth_token: str = Depends(oauth2_scheme)):

    try:
        user_data = await get_user_data_by_auth_token(auth_token)
    except jwt.JWTError:
        raise credentials_exception

    user = await User.get_or_none(id_=user_data["id_"])

    return user


# FIXME Delete crunch after we got sessions and users
with open(os.path.join(current_path, "test.json"), "r", encoding="utf8") as file:
    data = json.load(file)


@router.get("/all")
async def all_users():
    return data
