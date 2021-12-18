from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from modules import routers, database

app = FastAPI(
    title="ITMOCHART",
    description="ICT Hack #3 2021",
)
DB = database.MongoDbWrapper()

# app.include_router(router=routers.service_router, tags=["Service Endpoints"])
app.include_router(router=routers.user_router, tags=["User Management Endpoints"])
app.include_router(router=routers.chart_router, tags=["Chart Endpoints"])
