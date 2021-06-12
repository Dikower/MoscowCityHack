from datetime import datetime, timedelta
from typing import Optional

from jose import jws

from settings import SECRET_KEY


def generate_auth_token(user_id, expires_date: Optional[timedelta] = None):
    if expires_date is not None:
        expire = datetime.utcnow() + expires_date
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    return jws.sign({"id": user_id, "exp": expire}, SECRET_KEY, algorithm="HS256")


def check_auth_token(token):
    return jws.verify(token, SECRET_KEY, algorithms=["HS256"])
