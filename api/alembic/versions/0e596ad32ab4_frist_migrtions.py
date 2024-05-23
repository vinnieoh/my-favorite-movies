"""frist migrtions

Revision ID: 0e596ad32ab4
Revises: 
Create Date: 2024-05-23 13:07:05.123705

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum

# revision identifiers, used by Alembic.
revision: str = '0e596ad32ab4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enum para o tipo de mídia
class MediaType(Enum):
    MOVIE = "movie"
    TV_SHOW = "tv_show"

def upgrade() -> None:
    # Criação da tabela de usuários
    op.create_table(
        'usuarios',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('firstName', sa.String, nullable=False),
        sa.Column('lastName', sa.String, nullable=False),
        sa.Column('username', sa.String, nullable=False, unique=True, index=True),
        sa.Column('email', sa.String, nullable=False, unique=True, index=True),
        sa.Column('senha', sa.String, nullable=False)
    )
    
    # Criação da tabela de séries de TV
    op.create_table(
        'tv_shows',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('original_name', sa.String, nullable=True),
        sa.Column('first_air_date', sa.Date, nullable=True),
        sa.Column('origin_country', sa.String, nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('usuarios.id'))
    )

    # Criação da tabela de filmes
    op.create_table(
        'movies',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('original_title', sa.String, nullable=True),
        sa.Column('release_date', sa.Date, nullable=True),
        sa.Column('video', sa.Boolean, default=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('usuarios.id'))
    )

    # Criação da tabela de comentários
    op.create_table(
        'comments',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('media_id', sa.Integer, nullable=False),
        sa.Column('media_type', sa.Enum(MediaType), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False),
        sa.Column('updated_at', sa.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False),
        sa.Column('likes', sa.Integer, nullable=True, default=0)
    )

def downgrade() -> None:
    # Drop das tabelas
    op.drop_table('comments')
    op.drop_table('movies')
    op.drop_table('tv_shows')
    op.drop_table('usuarios')