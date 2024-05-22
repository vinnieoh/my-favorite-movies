from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.config.dependency import get_current_user, get_session

from app.schemas.movie_schemas import MovieCreateSchema, MovieUpdateSchema, MovieResponseSchema
from app.schemas.tv_shows_schemas import TVCreateSchema, TVUpdateSchema, TVResponseSchema

from app.models.tv_shows_model import TVModel
from app.models.movie_model import MovieModel
from app.models.usuario_model import UsuarioModel

from app.utils.request_api import (
    request_trading_all_week_br,
    request_trading_all_day_br,
    request_search_conteudo,
    request_movie_id,
    request_tv_show_id
)

router = APIRouter()


@router.get('/trending-all-week-br')
async def get_trending_all_week_br():
    
    resp = request_trading_all_week_br()
    
    if not resp:
         raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteudo não encontrado."
            )

    return resp
    

@router.get('/trading-all-day-br')
async def get_trading_all_day_br():
    
    resp = request_trading_all_day_br()

    if not resp:
         raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteudo não encontrado."
            )

    return resp


@router.get('/search-conteudo/{conteudo}')
async def get_search_conteudo(conteudo:str):
    
    resp = request_search_conteudo(conteudo)

    if not resp:
         raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteudo não encontrado."
            )

    return resp


@router.get('/movie-id/{id}', status_code=status.HTTP_200_OK)
async def get_movie_id(id: int):
    
    resp = request_movie_id(id)

    if not resp:
         raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteudo não encontrado."
            )

    return resp


@router.get('/tv-show-id/{id}', status_code=status.HTTP_200_OK)
async def get_tv_show_id(id: int):
    
    resp = request_tv_show_id(id)

    if not resp:
         raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteudo não encontrado."
            )

    return resp

"""@router.post('/registra-endereco', status_code=status.HTTP_201_CREATED, response_model=EnderecoSchema)
async def cria_endereco(endereco: EnderecoSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    novo_endereco: EnderecoModels = EnderecoModels(rua=endereco.rua, numero=endereco.numero, bairro=endereco.bairro, 
                                                    cep=endereco.cep, usuario_id=logado.id)

    async with db as session:
        try:
            session.add(novo_endereco)
            await session.commit()

            return novo_endereco
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Não foi possível cadastrar este endereço!')


@router.post('/registra-endereco', status_code=status.HTTP_201_CREATED, response_model=EnderecoSchema)
async def cria_endereco(endereco: EnderecoSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    novo_endereco: EnderecoModels = EnderecoModels(rua=endereco.rua, numero=endereco.numero, bairro=endereco.bairro, 
                                                    cep=endereco.cep, usuario_id=logado.id)

    async with db as session:
        try:
            session.add(novo_endereco)
            await session.commit()

            return novo_endereco
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Não foi possível cadastrar este endereço!')
"""