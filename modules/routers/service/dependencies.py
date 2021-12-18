from fastapi import HTTPException

from .models import AchievementTemplate
from ..user.models import User
from ...database import MongoDbWrapper

DB = MongoDbWrapper()


async def get_achievement_template(achievement_template_id: str) -> AchievementTemplate:
    """get requested achievement template"""
    try:
        return await DB.get_achievement_template_by_id(achievement_template_id)

    except KeyError as e:
        raise HTTPException(404, str(e))

    except Exception as e:
        raise HTTPException(500, str(e))


async def get_user_by_id(isu_id: str) -> User:
    """get requested user"""
    try:
        return await DB.get_user_by_isu_id(isu_id)

    except KeyError as e:
        raise HTTPException(404, str(e))

    except Exception as e:
        raise HTTPException(500, str(e))
