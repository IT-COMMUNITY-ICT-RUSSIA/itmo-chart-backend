import typing as tp

from pydantic import BaseModel
from datetime import datetime


class Subject(BaseModel):
    """Simple subject descriptor"""

    id: str
    name: str
    teachers: tp.List[str]


class Achievement(BaseModel):
    """Simple achievement descriptor"""

    id: str
    name: str
    type: str
    subject_id: tp.Optional[str] = None
    value: int
    timestamp: datetime


class AchievementEvent(BaseModel):
    """Achievement event descriptor"""

    id: str
    user_id: str
    timestamp: datetime
    achievement_id: str
    estimated_income: int
    balance_upon_receival: int


class Reward(BaseModel):
    """Simple reward descriptor"""

    id: str
    name: str
    price: int
    description: str
    thumbnail: str = "https://fund.itmo.family/webpack/production/assets/images/4.48ac80b5ad784b989366d69d7b5e335f.svg"
    count: int


class RewardEvent(BaseModel):
    """Reward event descriptor"""

    id: str
    reward_id: str
    user_id: str
    timestamp: datetime


class Subject(BaseModel):
    """Simple subject descriptor"""

    id: str
    faculty: str
    teachers: tp.List[str]
