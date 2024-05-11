from sqlalchemy import Column, String, Integer, Boolean, Date, Text, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.config.configs import settings

class BaseMediaModel(settings.DBBaseModel):
    __abstract__ = True  # Define que esta classe é abstrata e não será mapeada diretamente como uma tabela
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    original_id = Column(Integer, nullable=False, unique=True, index=True)
    original_language = Column(String, nullable=True)
    overview = Column(Text, nullable=True)
    popularity = Column(Float, nullable=True)
    vote_average = Column(Float, nullable=True)
    vote_count = Column(Integer, nullable=True)
    genre_ids = Column(Text, nullable=True) 
    backdrop_path = Column(String, nullable=True)
    poster_path = Column(String, nullable=True)
    is_adult = Column(Boolean, default=False)

class TVModel(BaseMediaModel):
    __tablename__ = 'tv_shows'
    name = Column(String, nullable=False)
    original_name = Column(String, nullable=True)
    first_air_date = Column(Date, nullable=True)
    origin_country = Column(String, nullable=True)

class MovieModel(BaseMediaModel):
    __tablename__ = 'movies'
    title = Column(String, nullable=False)
    original_title = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    video = Column(Boolean, default=False)
