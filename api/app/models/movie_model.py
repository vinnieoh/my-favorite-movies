from sqlalchemy import Column, String, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app.models.base_media_model import BaseMediaModel

class MovieModel(BaseMediaModel):
    __tablename__ = 'movies'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    original_title = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    video = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'))  # Chave estrangeira

    # Relacionamento com usuário
    user = relationship("UsuarioModel", back_populates="movies")