import typing as tp

from fastapi import APIRouter
from ...modules.models import GenericResponse

service_router = APIRouter()


@service_router.get("/achievement")
def get_user_achievements() -> GenericResponse:
    """"""
    pass


@service_router.post("/achievement")
def add_user_achievement() -> GenericResponse:
    pass


@service_router.update("/achievement")
def update_user_achievement() -> GenericResponse:
    pass


@service_router.get("/checkout")
def get_available_rewards() -> GenericResponse:
    pass


@service_router.post("/checkout")
def make_purchase() -> GenericResponse:
    pass


@service_router.get("/settings")
def get_current_settings() -> GenericResponse:
    pass


@service_router.update("/settings")
def update_settings() -> GenericResponse:
    pass
