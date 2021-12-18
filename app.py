import typing as tp
from fastapi import FastAPI

from modules import routers, database

api = FastAPI()
DB = database.MongoDbWrapper()


@api.get("/")
def get_status() -> tp.Dict[str, str]:
    return {"ok": True}


# api.include_router(router=routers.service_router, prefix="/service", tags=["Service Endpoints"])
api.include_router(router=routers.user_router, prefix="/user", tags=["User Management Enpoints"])
api.include_router(router=routers.chart_router, tags=["Chart Endpoints"])
