import os
import typing as tp
from datetime import datetime, timedelta

from pydantic import parse_obj_as
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from loguru import logger

from .routers.user.models import UserWithPassword, User

from .database import MongoDbWrapper
from .exceptions import CredentialsValidationException
from .models import TokenData

SECRET_KEY = os.environ.get("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return str(pwd_context.hash(password))


def create_access_token(
    data: tp.Dict[str, tp.Union[datetime, str]],
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(isu_number: str, password: str) -> tp.Optional[UserWithPassword]:
    user_data = await MongoDbWrapper().get_user_by_isu_id(isu_number)
    if not user_data:
        return None
    if not verify_password(password, user_data.hashed_password):
        return None
    return user_data


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    logger.info(f"got token {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(payload)
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsValidationException
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsValidationException

    try:
        user: UserWithPassword = await MongoDbWrapper().get_user_by_isu_id(token_data.username)
    except Exception as e:
        raise HTTPException(404, str(e))

    user_dict = user.dict(exclude={"hashed_password"})
    logger.info(f"user: {user_dict}")

    return parse_obj_as(User, user_dict)
