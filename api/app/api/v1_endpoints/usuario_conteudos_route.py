from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Union
from uuid import UUID

from app.models.tv_shows_model import TVModel
from app.models.movie_model import MovieModel
from app.models.usuario_model import UsuarioModel

from app.schemas.tv_shows_schemas import TVResponseSchema
from app.schemas.movie_schemas import MovieResponseSchema

from app.config.dependency import get_current_user, get_session

router = APIRouter()


@router.get('/conteudos', response_model=List[Union[MovieResponseSchema, TVResponseSchema]], status_code=status.HTTP_200_OK)
async def get_all_contents(logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        # Filmes
        movie_query = select(MovieModel).filter(MovieModel.user_id == logado.id)
        movie_result = await session.execute(movie_query)
        movies = movie_result.scalars().all()

        # Séries de TV
        tv_show_query = select(TVModel).filter(TVModel.user_id == logado.id)
        tv_show_result = await session.execute(tv_show_query)
        tv_shows = tv_show_result.scalars().all()

        # Unindo os resultados
        all_contents = movies + tv_shows

        if not all_contents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum conteúdo encontrado para este usuário.')

        return all_contents


@router.get('/filmes', response_model=List[MovieResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_movies(logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MovieModel).filter(MovieModel.user_id == logado.id)
        result = await session.execute(query)
        movies = result.scalars().all()

        if not movies:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum filme encontrado para este usuário.')

        return movies


@router.get('/tvshows', response_model=List[TVResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_tv_shows(logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TVModel).filter(TVModel.user_id == logado.id)
        result = await session.execute(query)
        tv_shows = result.scalars().all()

        if not tv_shows:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhuma série de TV encontrada para este usuário.')

        return tv_shows