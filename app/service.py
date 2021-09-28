from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from api import routers
from config import Sqlite

service = FastAPI()

for router in routers:
    service.include_router(router)

register_tortoise(
    service,
    db_url=f'sqlite://{Sqlite.database}',
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
