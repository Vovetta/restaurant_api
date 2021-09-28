from typing import List

from fastapi import APIRouter

from api.restaurants import restaurants_router

routers: List[APIRouter] = [
    restaurants_router
]
