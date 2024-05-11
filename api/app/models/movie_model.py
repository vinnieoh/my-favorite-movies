from sqlalchemy import Column, String, Date, Boolean

from app.models.base_media_model import BaseMediaModel

class MovieModel(BaseMediaModel):
    __tablename__ = 'movies'
    title = Column(String, nullable=False)
    original_title = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    video = Column(Boolean, default=False)
