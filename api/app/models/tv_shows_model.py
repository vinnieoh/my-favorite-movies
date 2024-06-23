from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app.models.base_media_model import BaseMediaModel

class TVModel(BaseMediaModel):
    __tablename__ = 'tv_shows'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    original_name = Column(String, nullable=True)
    first_air_date = Column(Date, nullable=True)
    origin_country = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'))  # Chave estrangeira

    # Relacionamento com usuário
    user = relationship("UsuarioModel", back_populates="tv_shows")