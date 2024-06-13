from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.usuario_model import UsuarioModel
from .configs import settings
from .security_password import verificar_senha

# Configuração do esquema OAuth2
oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/usuario/login")

# Modelo Pydantic para o payload do token JWT
class TokenPayload(BaseModel):
    type: str
    exp: datetime
    iat: datetime
    sub: str

# Função para autenticar o usuário
async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    query = select(UsuarioModel).filter(UsuarioModel.email == email)
    result = await db.execute(query)
    usuario: UsuarioModel = result.scalars().unique().one_or_none()

    if usuario and verificar_senha(senha, usuario.senha):
        return usuario
    return None

# Função para criar o token JWT
def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = TokenPayload(
        type=tipo_token,
        exp=now + tempo_vida,
        iat=now,
        sub=str(sub)
    )
    return jwt.encode(payload.dict(), settings.JWT_SECRET, algorithm=settings.ALGORITHM)

# Função para criar um token de acesso
def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
