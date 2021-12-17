import typing as tp
from fastapi import FastAPI


api = FastAPI()


@api.get("/")
def get_status() -> tp.Dict[str, str]:
    return {"ok": True}
