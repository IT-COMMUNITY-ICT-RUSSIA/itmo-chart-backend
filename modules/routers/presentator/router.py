import typing as tp

from fastapi import APIRouter, status

from .models import Chart, ChartEntry
from ..user.models import User
from ...database import MongoDbWrapper
from ...models import GenericResponse

chart_router = APIRouter(prefix="/chart")
DB = MongoDbWrapper()


@chart_router.get("/", response_model=tp.Union[Chart, GenericResponse])  # type: ignore
async def get_leaderboard(
    megafaculty: tp.Optional[str] = None,
    faculty: tp.Optional[str] = None,
    program: tp.Optional[str] = None,
    group: tp.Optional[str] = None,
) -> tp.Union[Chart, GenericResponse]:
    """Get leaderboard by filter (megafaculty, faculty, program, group)"""

    try:
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

        chart_data: tp.List[ChartEntry] = []

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

        return Chart(
            status_code=status.HTTP_200_OK,
            detail=f"Success gathering chart of {len(chart_data)} rows.)",
            chart_data=chart_data[:100],
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
