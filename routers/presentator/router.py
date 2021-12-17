import typing as tp

from fastapi import APIRouter
from ...modules.models import GenericResponse

chart_router = APIRouter(prefix="/chart")


@chart_router.get("/")
def get_leaderboard(
    megafaculty: tp.Optional[str],
    faculty: tp.Optional[str],
    program: tp.Optional[str],
    group: tp.Optional[str],
) -> GenericResponse:
    """Get leaderboard by filter (megafaculty, faculty, program, group)"""
    pass
