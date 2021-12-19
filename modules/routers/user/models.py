import typing as tp
from datetime import datetime

from pydantic import BaseModel

from modules.models import GenericResponse
from modules.routers.service.models import RewardEvent


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


class UserWithPassword(User):
    hashed_password: str


class UserOut(GenericResponse):
    user: User


class UsersOut(GenericResponse):
    users: tp.List[User]


class AchievementEventOut(GenericResponse):
    title: str
    description: str
    teacher_name: str
    student_name: str
    points_income: int
    coins_income: int


class AchievementsOut(GenericResponse):
    achievements: tp.List[AchievementEventOut]


class PurchasesOut(GenericResponse):
    purchases: tp.List[RewardEvent]
