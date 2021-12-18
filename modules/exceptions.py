from fastapi import HTTPException, status
import typing as tp
from loguru import logger


class AuthException(HTTPException):
    """Exception caused by authorization failure"""

    def __init__(self, **kwargs: tp.Any) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Incorrect username or password"
        self.headers = {"WWW-Authenticate": "Bearer"}

        logger.warning(f"{self.detail} : {kwargs}")


class CredentialsValidationException(HTTPException):
    """Exception caused by credentials (login/pass) validation"""

    def __init__(self, details: tp.Optional[str] = None, **kwargs: tp.Any) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = details or "Could not validate credentials"
        self.headers = {"WWW-Authenticate": "Bearer"}

        logger.warning(f"{self.detail} : {kwargs}")
