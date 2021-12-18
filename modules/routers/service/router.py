import math
import typing as tp

from fastapi import APIRouter, Depends, status

from .dependencies import get_achievement_template, get_user_by_id
from .models import AchievementEvent, AchievementTemplate, AchievementTemplateList, RewardEvent, RewardList
from ..user.models import User
from ...database import MongoDbWrapper
from ...models import GenericResponse
from ...security import get_current_user

service_router = APIRouter(prefix="/service")
DB = MongoDbWrapper()


@service_router.get("/rewards", response_model=tp.Union[RewardList, GenericResponse])  # type: ignore
async def get_available_rewards() -> tp.Union[RewardList, GenericResponse]:
    """Get all available rewards"""
    try:
        rewards = await DB.get_all_rewards()
        return RewardList(rewards=rewards)

    except KeyError as e:
        return GenericResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        return GenericResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@service_router.post("/checkout", response_model=GenericResponse)
async def purchase_reward(reward_id: str, user: User = Depends(get_current_user)) -> GenericResponse:
    """Purchase reward, change user's balance"""
    try:
        reward = await DB.get_reward_by_id(reward_id)

        if user.coins < reward.price:
            return GenericResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient funds",
            )

        user.coins -= reward.price
        await DB.update_user_data(user)

        purchase_event = RewardEvent(
            reward_id=reward.id,
            user_id=user.isu_id,
        )
        await DB.add_reward_event(purchase_event)

        return GenericResponse(detail="Purchase was successful")

    except KeyError as e:
        return GenericResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        return GenericResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@service_router.get("/achievements", response_model=tp.Union[AchievementTemplateList, GenericResponse])  # type: ignore
async def get_achievement_templates() -> tp.Union[AchievementTemplateList, GenericResponse]:
    """Get all available achievement templates"""
    try:
        achievements = await DB.get_all_achievements()
        return AchievementTemplateList(achievement_templates=achievements)

    except KeyError as e:
        return GenericResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        return GenericResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@service_router.post("/achievements", response_model=GenericResponse)
async def add_user_achievement(
    achievement: AchievementTemplate = Depends(get_achievement_template),
    student: User = Depends(get_user_by_id),
    teacher: User = Depends(get_current_user),
) -> GenericResponse:
    """Add new achievement, associated with concrete user"""
    try:
        student.points += achievement.value
        student.coins += math.ceil(achievement.value * 0.2)
        await DB.update_user_data(student)

        achievement_event = AchievementEvent(
            user_id=student.isu_id,
            creator_id=teacher.isu_id,
            achievement_id=achievement.id,
            estimated_income=achievement.value,
            balance_upon_receival=student.coins,
        )
        await DB.add_achievement_event(achievement_event)

        return GenericResponse(detail="Achievement assigned successful")

    except KeyError as e:
        return GenericResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        return GenericResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
