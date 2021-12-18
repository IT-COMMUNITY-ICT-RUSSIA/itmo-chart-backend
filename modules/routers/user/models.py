import typing as tp
from datetime import datetime

from pydantic import BaseModel

from modules.models import GenericResponse
from modules.routers.service.models import AchievementEvent


class User(BaseModel):
    """Simple user descriptor"""

    name: str
    birth_date: datetime
    isu_id: str
    date_created: datetime
    permissions: tp.List[str]
    megafaculty: str
    is_teacher: bool
    faculty: str
    program: tp.Optional[str]
    group: tp.Optional[str] = None
    points: int = 0
    coins: int = 0


class UserOut(GenericResponse):
    user: User


class UsersOut(GenericResponse):
    users: tp.List[User]


class AchievementsOut(GenericResponse):
    achievements: tp.List[AchievementEvent]
