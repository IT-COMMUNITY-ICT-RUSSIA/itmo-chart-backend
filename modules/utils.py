from datetime import datetime, timedelta
import typing as tp
import random

from faker import Faker
from faker.providers import DynamicProvider

from modules.routers.user.models import UserWithPassword
from app import DB

# from .. import routers


university_structure = {
    "МФ ТИНТ": {
        "ФИКТ": {
            "Прикладная информатика": "K3141",
            "Инфокоммуникационные технологии и системы связи": "K3121",
        },
        "ФИТИП": {
            "Прикладная математика и информатика": "M3138",
            "Информационные системы и технологии": "M3105",
        },
    },
    "МФ КТУ": {
        "ФПИиКТ": {
            "Информатика и вычислительная техника": "P3132",
            "Программная инженерия": "P3120",
        },
        "ФБИТ": {
            "Информационная безопасность": "N3145",
            "Конструирование и технология электронных средств": "N3156",
        },
        "ФСУиР": {"Робототехника": "R3135", "Приборостроение": "R4157"},
    },
    "ФТ МФ": {
        "ИИФ": {"Оптотехника": "B3100"},
        "ФФ": {"Фотоника и оптоинформатика": "L3122", "Техническая физика": "L3199"},
    },
}


Student = tp.Dict[str, tp.Union[int, str, bool]]


def gen_datetime(min_year: int = 2001, max_year=2003):
    start = datetime(min_year, 1, 1)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def generate_fake_student(context: tp.Optional[tp.Dict[str, str]] = None) -> Student:
    fake_data = Faker(locale=["ru_RU"])
    if not context:
        megafaculty: str = random.choice(list(university_structure))
        faculty: str = random.choice(list(university_structure[megafaculty]))
        program: str = random.choice(list(university_structure[megafaculty][faculty]))
        group: str = university_structure[megafaculty][faculty][program]
        context = {
            "megafaculty": megafaculty,
            "faculty": faculty,
            "program": program,
            "group": group,
        }
    return {
        "name": fake_data.name(),
        "birth_date": gen_datetime(),
        "isu_id": str(random.randint(0, 900001)),
        "date_created": gen_datetime(min_year=2017, max_year=2021),
        "permissions": ["read"],
        "is_teacher": False,
        "hashed_password": "$2b$12$QCa5qJRNt7qh5H.ooiznCebHzFx6obV4Koz0J.nwJ3TLiaZLWL4v6",
        **context,
    }


def generate_fake_group(context: tp.Optional[tp.Dict[str, str]] = None) -> tp.List[Student]:
    if not context:
        megafaculty: str = random.choice(list(university_structure))
        faculty: str = random.choice(list(university_structure[megafaculty]))
        program: str = random.choice(list(university_structure[megafaculty][faculty]))
        group: str = university_structure[megafaculty][faculty][program]
        context = {
            "megafaculty": megafaculty,
            "faculty": faculty,
            "program": program,
            "group": group,
        }
    return [generate_fake_student(context) for _ in range(15)]


def generate_fake_faculty(contexts: tp.Optional[tp.List[tp.Dict[str, str]]] = None) -> tp.Dict[str, tp.List[Student]]:
    if not contexts:
        megafaculty: str = random.choice(list(university_structure))
        faculty: str = random.choice(list(university_structure[megafaculty]))
        programs: str = list(university_structure[megafaculty][faculty].keys())
        groups: str = [university_structure[megafaculty][faculty][program] for program in programs]
        contexts = [
            {"megafaculty": megafaculty, "faculty": faculty, "program": program, "group": group}
            for group, program in zip(groups, programs)
        ]
    contexts_copy = contexts.copy()
    for context in contexts:
        contexts_copy[contexts_copy.index(context)]["students"] = generate_fake_group(context)
    return contexts_copy


def generate_fake_megafaculty(
    contexts: tp.Optional[tp.List[tp.Dict[str, str]]] = None
) -> tp.Dict[str, tp.Union[str, Student]]:
    if not contexts:
        megafaculty: str = random.choice(list(university_structure))
        facultys = list(university_structure[megafaculty].keys())
        programs = [university_structure[megafaculty][faculty] for faculty in facultys]
        contexts = [
            [
                {"megafaculty": megafaculty, "faculty": faculty, "program": pk, "group": pi}
                for faculty in facultys
                for pk, pi in zip(program.keys(), program.values())
            ]
            for program in programs
        ]
    contexts_copy = contexts.copy()[0]
    for context in contexts[0]:
        contexts_copy[contexts_copy.index(context)]["students"] = generate_fake_group(context)
    return contexts_copy


def generate_fake_university() -> tp.Dict[str, tp.Dict]:
    megafacultys: str = list(university_structure)
    students = []
    [
        [
            [
                students.extend(
                    generate_fake_group(
                        {
                            "megafaculty": megafaculty,
                            "faculty": faculty,
                            "program": program,
                            "group": university_structure[megafaculty][faculty][program],
                        }
                    )
                )
                for program in university_structure[megafaculty][faculty]
            ]
            for faculty in university_structure[megafaculty]
        ]
        for megafaculty in megafacultys
    ]
    return students
