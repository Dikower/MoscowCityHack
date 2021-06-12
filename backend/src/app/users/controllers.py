import json
import os
import traceback
from datetime import timedelta
from enum import Enum
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
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


class LoginOptions(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    GITHUB = "github"
    SBERID = "sberid"


class LoginData(BaseModel):
    login_method: LoginOptions
    fio: str
    profile_picture: Optional[str] = None

    class Config:
        use_enum_values = True


@router.post("/login")
async def login(login_data: LoginData, request: Request):

    if login_data.login_method == LoginOptions.EMAIL.value:
        user_token = await generate_auth_token(
            uuid4(),
            **login_data.dict(),
            expires_date=timedelta(minutes=5),
        )
        login_link = request.url_for("auth", **{"auth_token": user_token})
        # TODO send to email
        return login_link
    else:
        return "NO known login method"


@router.get("/auth/{auth_token}")
async def auth(auth_token: str):
    # TODO invalidate token after using

    try:
        user_data = await get_user_data_by_auth_token(auth_token)
    except jwt.JWTError:
        raise credentials_exception

    user_id = uuid4()
    auth_token = await generate_auth_token(user_id)

    await User.create(
        id_=user_id,
        fio=user_data.get("fio"),
        auth_token=auth_token,
        profile_pic=user_data.get("profile_picture"),
    )

    return auth_token


@router.post("/users/get_me")
async def get_me(auth_token: str = Depends(oauth2_scheme)):

    try:
        user_data = await get_user_data_by_auth_token(auth_token)
    except jwt.JWTError:
        traceback.print_exc()
        raise credentials_exception

    user = await User.get_or_none(id_=user_data["id"])

    return user


# FIXME Delete crunch after we got sessions and users
with open(os.path.join(current_path, "test.json"), "r", encoding="utf8") as file:
    data = json.load(file)


@router.get("/all")
async def all_users():
    return data
