from datetime import datetime, timedelta
import typing as tp
import random

from faker import Faker
from faker.providers import DynamicProvider


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


def gen_datetime(min_year: int = 2001, max_year=2003):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()


def generate_fake_student():
    fake_data = Faker(locale=["ru_RU"])
    megafaculty: str = random.choice(list(university_structure))
    faculty: str = random.choice(list(university_structure[megafaculty]))
    program: str = random.choice(list(university_structure[megafaculty][faculty]))
    group: str = university_structure[megafaculty][faculty]
    return {
        "name": fake_data.name(),
        "birth_date": gen_datetime(),
        "isu_id": random.randint(0, 500001),
        "date_created": gen_datetime(min_year=2017, max_year=2021),
        "permissions": ["read"],
        "megafaculty": megafaculty,
        "is_teacher": False,
        "faculty": faculty,
        "program": program,
        "group": group,
    }


print(generate_fake_student())
