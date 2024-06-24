from sqlalchemy import Column, Text, DateTime, Integer, ForeignKey, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum
from app.config.configs import settings

class CommentModel(settings.DBBaseModel):
    __tablename__ = 'comments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False)
    media_id = Column(Integer, nullable=False)
    media_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    likes = Column(Integer, nullable=True, default=0)

    # Relationships
    user = relationship("UsuarioModel", back_populates="comments")
