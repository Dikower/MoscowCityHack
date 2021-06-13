import json
import os
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
from .mailer import send_mail

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
    fio: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        use_enum_values = True


@router.post("/login")
async def login(login_data: LoginData, request: Request):

    if login_data.login_method == LoginOptions.EMAIL.value:
        user_token = await generate_auth_token(
            uuid4(),
            **login_data.dict(),  # TODO redaundant values
            expires_date=timedelta(minutes=5),
        )
        login_link = request.url_for("auth", **{"auth_token": user_token})
        send_mail(login_link, login_data.email)
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

    print(await User.all())
    user = await User.get_or_none(email=user_data.get("email"))

    # если пользователь и токен уже существуют
    if user and user.auth_token:
        try:
            await get_user_data_by_auth_token(user.auth_token)
        except jwt.ExpiredSignatureError:
            # перегенерируем токен если он протух
            user_auth_token = await generate_auth_token(user.id)
            await user.update_from_dict({"auth_token": user_auth_token})
            await user.save()

        # возвращаем токен
        return user.auth_token

    # если юзер есть но токена нет, то генерируем токен
    elif user and not user.auth_token:
        user_auth_token = await generate_auth_token(user.id)
        await user.update_from_dict({"auth_token": user_auth_token})
        await user.save()
        return user_auth_token

    # создаем нового юзера если его нет в базе
    user_id = uuid4()
    user_auth_token = await generate_auth_token(user_id)

    await User.create(
        id=user_id,
        fio=user_data.get("fio"),
        email=user_data.get("email"),
        auth_token=user_auth_token,
        avatar=user_data.get("avatar"),
    )

    return auth_token


@router.post("/get_me")
async def get_me(auth_token: str = Depends(oauth2_scheme)):

    try:
        user_data = await get_user_data_by_auth_token(auth_token)
    except jwt.JWTError:
        raise credentials_exception

    user = await User.get_or_none(id=user_data["id"])

    if not user.auth_token:
        return "Found you, evil hacker!"
        # залогировать злобного хакера

    return user


@router.post("/logout")
async def logout(auth_token: str = Depends(oauth2_scheme)):

    user = await User.get_or_none(auth_token=auth_token)

    if user:
        await user.update_from_dict({"auth_token": None})
        await user.save()
    else:
        return "already logged out"

    return user


# FIXME Delete crunch after we got sessions and users
with open(os.path.join(current_path, "test.json"), "r", encoding="utf8") as file:
    data = json.load(file)


@router.get("/all")
async def all_users():
    return data
