from __future__ import annotations

import typing as tp

from pydantic import BaseModel


class GenericResponse(BaseModel):
    status_code: int = 200
    detail: tp.Optional[str] = "Successful"


class User(BaseModel):
    username: str
    is_admin: bool = False


class UserWithPassword(User):
    hashed_password: str


class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
