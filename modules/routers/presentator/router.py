import time
import typing as tp

import redis
from fastapi import APIRouter, status
from loguru import logger
from pydantic import parse_obj_as

from .models import Chart, ChartEntry
from ..user.models import User
from ...database import MongoDbWrapper
from ...models import GenericResponse

chart_router = APIRouter(prefix="/chart")
DB = MongoDbWrapper()
REDIS = redis.Redis(host="redis", socket_connect_timeout=3)


def _is_in_cache(query: tp.Tuple[str, str, str, str]) -> bool:
    """check if query is available in cache"""
    return REDIS.exists(str(query))


def _cache_to_redis(query: tp.Tuple[str, str, str, str], chart_data: tp.List[ChartEntry]) -> None:
    """save chart data to redis"""
    ttl = 60 ** 2
    REDIS.set(
        name=str(query),
        value=repr([entry.dict() for entry in chart_data]),
        exat=int(time.time()) + ttl,
    )
    logger.info(f"cache added to redis. set to expire after {ttl}s.")


def _unpack_from_redis(query: tp.Tuple[str, str, str, str]) -> tp.List[ChartEntry]:
    """het chart data to redis"""
    data = eval(REDIS.get(name=str(query)))
    return [parse_obj_as(ChartEntry, entry) for entry in data]


@chart_router.get("/", response_model=tp.Union[Chart, GenericResponse])  # type: ignore
async def get_leaderboard(
    megafaculty: tp.Optional[str] = None,
    faculty: tp.Optional[str] = None,
    program: tp.Optional[str] = None,
    group: tp.Optional[str] = None,
) -> tp.Union[Chart, GenericResponse]:
    """Get leaderboard by filter (megafaculty, faculty, program, group)"""

    try:
        query = (megafaculty, faculty, program, group)

        if REDIS.exists(str(query)):
            logger.info("cache will be pulled from redis")
            chart_data: tp.List[ChartEntry] = _unpack_from_redis(query)
            logger.info("cache pulled successfully")
        else:
            if group is not None:
                students: tp.List[User] = await DB.get_all_students_by_group(group)
            elif program is not None:
                students = await DB.get_all_students_by_program(program)
            elif faculty is not None:
                students = await DB.get_all_students_by_faculty(faculty)
            elif megafaculty is not None:
                students = await DB.get_all_students_by_megafaculty(megafaculty)
            else:
                students = await DB.get_all_students()

            if not students:
                raise KeyError("Nothing to display")

            students.sort(key=lambda u: u.points, reverse=True)

            chart_data = []

            for position, student in enumerate(students, start=1):
                entry = ChartEntry(
                    name=student.name,
                    megafaculty=str(student.megafaculty),
                    faculty=str(student.faculty),
                    program=str(student.program),
                    group=str(student.group),
                    points=student.points,
                    rating_position=position,
                )

                chart_data.append(entry)

                if position >= 100:
                    break

            _cache_to_redis(query, chart_data)

        return Chart(
            status_code=status.HTTP_200_OK,
            detail=f"Success gathering chart of {len(chart_data)} rows",
            chart_data=chart_data,
        )

    except KeyError as e:
        return GenericResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No matching results found for the provided query. {e}",
        )

    except Exception as e:
        return GenericResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred: {e}",
        )
