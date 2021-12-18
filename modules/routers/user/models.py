import typing as tp
from datetime import datetime

from pydantic import BaseModel


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
