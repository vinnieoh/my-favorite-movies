from fastapi import APIRouter

from .v1_endpoints import usuario_route
from .v1_endpoints import comentario_route
from .v1_endpoints import conteudos_route

api_router = APIRouter()

api_router.include_router(usuario_route.router, prefix='/usuario', tags=['usuario'])
api_router.include_router(conteudos_route.router, prefix='/conteudos', tags=['conteudos'])
api_router.include_router(comentario_route.router, prefix='/comentario', tags=['comentario'])
