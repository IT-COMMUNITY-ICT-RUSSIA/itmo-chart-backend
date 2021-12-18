import typing as tp
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field
from ...models import GenericResponse


class Subject(BaseModel):
    """Simple subject descriptor"""

    name: str
    teachers: tp.List[str]
    id: str = Field(default_factory=lambda: uuid4().hex)


class AchievementTemplate(BaseModel):
    """Simple achievement descriptor"""

    name: str
    type: str
    value: int
    timestamp: datetime = Field(default_factory=datetime.now)
    subject_id: tp.Optional[str] = None
    id: str = Field(default_factory=lambda: uuid4().hex)


class AchievementEvent(BaseModel):
    """Achievement event descriptor"""

    user_id: str
    creator_id: str
    achievement_id: str
    estimated_income: int
    balance_upon_receival: int
    timestamp: datetime = Field(default_factory=datetime.now)
    id: str = Field(default_factory=lambda: uuid4().hex)


class Reward(BaseModel):
    """Simple reward descriptor"""

    name: str
    price: int
    description: str
    count: int = 1
    thumbnail: str = "https://fund.itmo.family/webpack/production/assets/images/4.48ac80b5ad784b989366d69d7b5e335f.svg"
    id: str = Field(default_factory=lambda: uuid4().hex)


class RewardList(GenericResponse):
    rewards: tp.List[Reward]


class AchievementTemplateList(GenericResponse):
    achievement_templates: tp.List[AchievementTemplate]


class RewardEvent(BaseModel):
    """Reward event descriptor"""

    reward_id: str
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    id: str = Field(default_factory=lambda: uuid4().hex)
