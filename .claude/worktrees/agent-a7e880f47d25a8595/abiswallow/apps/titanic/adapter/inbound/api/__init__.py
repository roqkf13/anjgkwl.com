from fastapi import APIRouter

from titanic.adapter.inbound.api.v1.james_director_router import james_director_router
from titanic.adapter.inbound.api.v1.walter_roaster_router import walter_roaster_router

titanic_router = APIRouter()
titanic_router.include_router(james_director_router)
titanic_router.include_router(walter_roaster_router)

titanic_routers = [titanic_router]
