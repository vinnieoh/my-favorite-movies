from fastapi import APIRouter

from .v1_endpoints import usuario_route


api_router = APIRouter()

api_router.include_router(usuario_route.router, prefix='/usuario', tags=['usuario'])