from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
    

@router.get('/trending-all-day-br')
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

@router.post('/registra-filme', status_code=status.HTTP_201_CREATED, response_model=MovieCreateSchema)
async def cria_filme(filme: MovieCreateSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    
    novo_filme = MovieModel(
        original_id=filme.original_id,
        original_language=filme.original_language,
        overview=filme.overview,
        popularity=filme.popularity,
        vote_average=filme.vote_average,
        vote_count=filme.vote_count,
        genre_ids=filme.genre_ids,
        backdrop_path=filme.backdrop_path,
        poster_path=filme.poster_path,
        is_adult=filme.is_adult,
        title=filme.title,
        original_title=filme.original_title,
        release_date=filme.release_date,
        video=filme.video,
        user_id=logado.id
    )

    async with db as session:
        try:
            session.add(novo_filme)
            await session.commit()
            await session.refresh(novo_filme)
            return novo_filme
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                detail='Não foi possível cadastrar este filme!'
            ) 


@router.post('/registra-tvshow', status_code=status.HTTP_201_CREATED, response_model=TVCreateSchema)
async def cria_tvshow(tv_show: TVCreateSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    
    novo_tv_show = TVModel(
        original_id=tv_show.original_id,
        original_language=tv_show.original_language,
        overview=tv_show.overview,
        popularity=tv_show.popularity,
        vote_average=tv_show.vote_average,
        vote_count=tv_show.vote_count,
        genre_ids=tv_show.genre_ids,
        backdrop_path=tv_show.backdrop_path,
        poster_path=tv_show.poster_path,
        is_adult=tv_show.is_adult,
        name=tv_show.name,
        original_name=tv_show.original_name,
        first_air_date=tv_show.first_air_date,
        origin_country=tv_show.origin_country,
        user_id=logado.id
    )

    async with db as session:
        try:
            session.add(novo_tv_show)
            await session.commit()
            await session.refresh(novo_tv_show)
            return novo_tv_show
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                detail='Não foi possível cadastrar este TV show!'
            )
            

@router.delete('/delete-filme/{filme_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_filme(filme_id: str, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MovieModel).filter(MovieModel.id == filme_id)
        result = await session.execute(query)
        filme_del = result.scalars().unique().one_or_none()
        
        if not filme_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Filme não encontrado.')
        
        # Verificar se o usuário logado tem permissão para deletar este filme
        if logado.id != filme_del.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a deletar este filme.")
        
        await session.delete(filme_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/delete-tvshow/{tv_show_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tv_show(tv_show_id: str, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TVModel).filter(TVModel.id == tv_show_id)
        result = await session.execute(query)
        tv_show_del = result.scalars().unique().one_or_none()
        
        if not tv_show_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='TV show não encontrado.')
        
        # Verificar se o usuário logado tem permissão para deletar este TV show
        if logado.id != tv_show_del.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a deletar este TV show.")
        
        await session.delete(tv_show_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put('/update-filme/{filme_id}', response_model=MovieUpdateSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_filme(filme_id: str, filme: MovieUpdateSchema, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MovieModel).filter(MovieModel.id == filme_id)
        result = await session.execute(query)
        filme_up = result.scalars().one_or_none()

        if not filme_up:
            raise HTTPException(detail='Filme não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
        # Verificar se o usuário logado tem permissão para atualizar este filme
        if logado.id != filme_up.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este filme.")
        
        # Atualização de campos condicional
        if filme.title:
            filme_up.title = filme.title
        if filme.original_title:
            filme_up.original_title = filme.original_title
        if filme.release_date:
            filme_up.release_date = filme.release_date
        if filme.video is not None:
            filme_up.video = filme.video
        if filme.original_id:
            filme_up.original_id = filme.original_id
        if filme.original_language:
            filme_up.original_language = filme.original_language
        if filme.overview:
            filme_up.overview = filme.overview
        if filme.popularity:
            filme_up.popularity = filme.popularity
        if filme.vote_average:
            filme_up.vote_average = filme.vote_average
        if filme.vote_count:
            filme_up.vote_count = filme.vote_count
        if filme.genre_ids:
            filme_up.genre_ids = filme.genre_ids
        if filme.backdrop_path:
            filme_up.backdrop_path = filme.backdrop_path
        if filme.poster_path:
            filme_up.poster_path = filme.poster_path
        if filme.is_adult is not None:
            filme_up.is_adult = filme.is_adult

        await session.commit()
        return filme_up


@router.put('/update-tvshow/{tv_show_id}', response_model=TVUpdateSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_tv_show(tv_show_id: str, tv_show: TVUpdateSchema, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TVModel).filter(TVModel.id == tv_show_id)
        result = await session.execute(query)
        tv_show_up = result.scalars().one_or_none()

        if not tv_show_up:
            raise HTTPException(detail='TV show não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
        # Verificar se o usuário logado tem permissão para atualizar este TV show
        if logado.id != tv_show_up.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este TV show.")
        
        # Atualização de campos condicional
        if tv_show.name:
            tv_show_up.name = tv_show.name
        if tv_show.original_name:
            tv_show_up.original_name = tv_show.original_name
        if tv_show.first_air_date:
            tv_show_up.first_air_date = tv_show.first_air_date
        if tv_show.origin_country:
            tv_show_up.origin_country = tv_show.origin_country
        if tv_show.original_id:
            tv_show_up.original_id = tv_show.original_id
        if tv_show.original_language:
            tv_show_up.original_language = tv_show.original_language
        if tv_show.overview:
            tv_show_up.overview = tv_show.overview
        if tv_show.popularity:
            tv_show_up.popularity = tv_show.popularity
        if tv_show.vote_average:
            tv_show_up.vote_average = tv_show.vote_average
        if tv_show.vote_count:
            tv_show_up.vote_count = tv_show.vote_count
        if tv_show.genre_ids:
            tv_show_up.genre_ids = tv_show.genre_ids
        if tv_show.backdrop_path:
            tv_show_up.backdrop_path = tv_show.backdrop_path
        if tv_show.poster_path:
            tv_show_up.poster_path = tv_show.poster_path
        if tv_show.is_adult is not None:
            tv_show_up.is_adult = tv_show.is_adult

        await session.commit()
        return tv_show_up
