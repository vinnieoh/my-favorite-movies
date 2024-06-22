from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.sql import text

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models.usuario_model import UsuarioModel
from app.schemas.usuario_schemas import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate, UsuarioIdSchemas, UsuarioSchemaEmail
from app.config.dependency import get_current_user, get_session
from app.config.security_password import gerar_hash_senha
from app.config.auth import autenticar, criar_token_acesso

router = APIRouter()

# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')
        
    response_content = {
        "id": str(usuario.id),  # Converte o UUID para string
        "username": usuario.username,
        "email": usuario.email,
        "token": criar_token_acesso(sub=usuario.id),
        "token_type": "bearer"
    }

    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)
    

# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario = UsuarioModel(
        firstName=usuario.firstName,
        lastName=usuario.lastName,
        username=usuario.username,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha)
    )
    
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except IntegrityError:
            await session.rollback()  # Importante para garantir o estado da transação
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='Já existe um usuário com este email ou username cadastrado.'
            )


@router.get('/usuario-id/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario_id(usuario_id: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.get('/usuario-email/{email_id}', response_model=UsuarioSchemaEmail, status_code=status.HTTP_200_OK)
async def get_usuario_email(email_id: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        
        query_email = select(UsuarioModel).filter(UsuarioModel.email == str(email_id.replace("%40", "@")))
        result = await session.execute(query_email)
        usuario: UsuarioSchemaEmail = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# GET Usuarios
@router.get('/', response_model=List[UsuarioIdSchemas])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioIdSchemas] = result.scalars().unique().all()

        return usuarios


# PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: str, usuario: UsuarioSchemaUpdate, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up = result.scalars().one_or_none()

        if not usuario_up:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
        # Verificar se o usuário logado tem permissão para atualizar este usuário
        if logado.id != usuario_up.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este usuário.")
        
        # Atualização de campos condicional
        if usuario.firstName:
            usuario_up.firstName = usuario.firstName
        if usuario.lastName:
            usuario_up.lastName = usuario.lastName
        if usuario.username:
            usuario_up.username = usuario.username
        if usuario.email:
            usuario_up.email = usuario.email
        if usuario.senha:
            usuario_up.senha = gerar_hash_senha(usuario.senha)
        
        await session.commit()
        return usuario_up



# DELETE usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: str, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaUpdate = result.scalars().unique().one_or_none()
        
        if not usuario_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')
        
        # Verificar se o usuário logado tem permissão para atualizar este usuário
        if logado.id != usuario_del.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este usuário.")
        

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)