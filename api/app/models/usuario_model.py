from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.config.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    senha = Column(String, nullable=False)

    # Relacionamento com comentários
    comments = relationship("CommentModel", back_populates="user")
    
    # Relacionamento com filmes
    movies = relationship("MovieModel", back_populates="user")
    
    # Relacionamento com programas de TV
    tv_shows = relationship("TVModel", back_populates="user")