import json
import os
from datetime import timedelta
from enum import Enum
from typing import Optional, List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status, Body
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel
from .schemas import PublicUser
from ..auth_helpers import generate_auth_token, get_user_data_by_auth_token
from .models import User, Token
from .mailer import send_mail
from ..settings import IS_PROD

current_path = os.path.dirname(os.path.realpath(__file__))

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

token_expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
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


async def get_user(auth_token=Depends(oauth2_scheme)):
    try:
        user_data = await get_user_data_by_auth_token(auth_token)
    except jwt.JWTError:
        raise credentials_exception
    user = await User.get_or_none(id=user_data["id"])
    if user is None:
        raise HTTPException(404, 'User not found')
    return user


class AfterLogin(BaseModel):
    url: str
    token: str


@router.post("/login", response_model=AfterLogin)
async def login(login_data: LoginData):
    if login_data.login_method == LoginOptions.EMAIL.value:

        user_token = await generate_auth_token(
            uuid4(),
            **login_data.dict(),  # TODO redaundant values
            expires_date=timedelta(minutes=5),
        )

        await Token.create(login_token=user_token)

        # login_link = request.url_for("auth", **{"auth_token": user_token})
        login_link = f'http://localhost:5000/{user_token}'
        # if IS_PROD:
        #     login_link = f''
        # send_mail(login_link, login_data.email)

        return AfterLogin(url=login_link, token=user_token)
    else:
        return "NO known login method"


class AuthToken(BaseModel):
    token: str


@router.post("/auth", response_model=AuthToken)
async def auth(auth_token: AuthToken):
    # если токен уже существует, второй раз он не сработает
    stored_token = await Token.get_or_none(login_token=auth_token.token)
    if stored_token:
        if stored_token.is_used:
            raise token_expired_exception
        else:
            await stored_token.update_from_dict({"is_used": True})
            await stored_token.save()

    try:
        user_data = await get_user_data_by_auth_token(auth_token.token)
    except jwt.JWTError:
        raise credentials_exception

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
        return AuthToken(token=user.auth_token)

    # если юзер есть но токена нет, то генерируем токен
    elif user and not user.auth_token:
        user_auth_token = await generate_auth_token(user.id)
        await user.update_from_dict({"auth_token": user_auth_token})
        await user.save()
        return AuthToken(token=user_auth_token)

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

    return AuthToken(token=user_auth_token)


@router.get("/get_me")
async def get_me(auth_token: str = Depends(oauth2_scheme)):
    try:
        user_data = await get_user_data_by_auth_token(auth_token)
    except jwt.JWTError:
        raise credentials_exception

    user = await User.get_or_none(id=user_data["id"])
    if user is None:
        raise HTTPException(404, 'User not found')

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


@router.get("/all", response_model=List[PublicUser])
async def all_users():
    return await PublicUser.from_queryset(User.all())
