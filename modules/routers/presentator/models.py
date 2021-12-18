import typing as tp
from datetime import datetime

from pydantic import BaseModel, Field

from ...models import GenericResponse


class ChartEntry(BaseModel):
    """a single row in a chart table"""

    name: str
    megafaculty: str
    faculty: str
    program: str
    group: str
    points: int = 0
    rating_position: int = 0


class Chart(GenericResponse):
    """chart source data"""

    chart_data: tp.List[ChartEntry]
    generated_at: str = Field(default_factory=lambda: str(datetime.now()))
