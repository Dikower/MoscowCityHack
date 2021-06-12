import json
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from jose import jwt
from starlette import status

from ..settings import SECRET_KEY
from .models import User

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

router = APIRouter()


async def _generate_auth_token(user_id, expires_date: Optional[timedelta] = None):
    if expires_date is not None:
        expire = datetime.utcnow() + expires_date
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    return jwt.encode({"id": user_id, "exp": expire}, SECRET_KEY, algorithm="HS256")


async def _get_user_by_auth_token(token):
    user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user = await User.get_or_none(id_=user_data["id_"])
    return user


# TODO make models
@router.post("/users/auth")
async def login(auth_method: str):
    user = await User.create(id_=uuid4(), fio="Zalupkin A. I")
    user_token = _generate_auth_token(user.id_)
    return 1


# FIXME Delete crunch after we got sessions and users
with open("users/test.json", "r", encoding="utf8") as file:
    data = json.load(file)


@router.get("/all")
async def all_users():
    return data
