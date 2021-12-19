import math
import typing as tp

from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from modules.database import MongoDbWrapper

from ...exceptions import AuthException
from ...models import GenericResponse, Token
from ...routers.user.models import AchievementsOut, RewardEventOut, User, UserOut, UsersOut, PurchasesOut, \
    AchievementEventOut
from ...security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
)

user_router = APIRouter(prefix="/user")


@user_router.post("/login", response_model=tp.Union[Token, GenericResponse])  # type: ignore
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    log the user in provided the username
    and password and return a JWT token
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed to login user {form_data.username}")
        raise AuthException
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.isu_id}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@user_router.get("/me", response_model=tp.Union[UserOut, GenericResponse])  # type: ignore
async def get_user_data(user: User = Depends(get_current_user)) -> UserOut:
    """return data for the requested user"""
    return UserOut(user=user)


@user_router.get("/users", response_model=tp.Union[UsersOut, GenericResponse])  # type: ignore
async def get_all_users(user: User = Depends(get_current_user)) -> tp.Union[UsersOut, GenericResponse]:
    """get all known users"""
    if not (user.is_teacher and "write" in user.permissions):
        return GenericResponse(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    users = await MongoDbWrapper().get_all_users()
    return UsersOut(users=users)


@user_router.get("/achievements", response_model=tp.Union[AchievementsOut, GenericResponse])  # type: ignore
async def get_user_achievements(student: User = Depends(get_current_user)) -> AchievementsOut:
    """return achievement data for the requested user"""
    try:
        achievements = await MongoDbWrapper().get_all_recieved_achievements_for_user(student)
        achievement_cards = []

        for event in achievements:
            achievement_template = await MongoDbWrapper().get_achievement_template_by_id(event.achievement_id)
            teacher = await MongoDbWrapper().get_user_by_isu_id(event.creator_id)
            card = AchievementEventOut(
                title=achievement_template.name,
                description=achievement_template.type,
                teacher_name=teacher.name,
                student_name=student.name,
                points_income=event.estimated_income,
                coins_income=math.ceil(event.estimated_income * 0.2),
            )
            achievement_cards.append(card)
    except KeyError as e:
        logger.error(str(e))
        achievement_cards = []

    return AchievementsOut(achievements=achievement_cards)


@user_router.get("/purchase-history", response_model=PurchasesOut)
async def get_user_achievements(user: User = Depends(get_current_user)) -> PurchasesOut:
    """return purchase data for the requested user"""
    try:
        rewards = await MongoDbWrapper().get_all_reward_events_for_user(user=user)
    except KeyError:
        rewards = []

    reward_cards = []
    for event in rewards:
        reward_template = await MongoDbWrapper().get_reward_by_id(event.reward_id)
        card = RewardEventOut(
            title=reward_template.name,
            thumbnail=reward_template.thumbnail,
            price=reward_template.price,
            timestamp=event.timestamp,
            buyer_name=user.name,
        )
        reward_cards.append(card)

    return PurchasesOut(purchases=reward_cards)
