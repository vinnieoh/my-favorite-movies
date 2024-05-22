from typing import  Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from .database import Session
from .auth import oauth2_schema
from .configs import settings
from app.models.usuario_model import UsuarioModel

class TokenData(BaseModel):
    user_id: Optional[str] = None

async def get_session() -> Generator: # type: ignore
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()

def create_credential_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"}
    )

async def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise create_credential_exception()
        return TokenData(user_id=str(user_id))
    except JWTError:
        raise create_credential_exception()

async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)) -> UsuarioModel:
    token_data = await decode_token(token)
    query = select(UsuarioModel).filter(UsuarioModel.id == token_data.user_id)
    result = await db.execute(query)
    user = result.scalars().one_or_none()
    if user is None:
        raise create_credential_exception()
    return user
