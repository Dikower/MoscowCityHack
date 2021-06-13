from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from ..settings import SECRET_KEY


async def generate_auth_token(user_id, expires_date: Optional[timedelta] = None, **custom_fileds):
    if expires_date is not None:
        expire = datetime.utcnow() + expires_date
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    return jwt.encode({"id": str(user_id), "exp": expire, **custom_fileds}, SECRET_KEY, algorithm="HS256")


async def get_user_data_by_auth_token(token):
    user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return user_data
