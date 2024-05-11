from sqlalchemy import Column, String, Date

from app.models.base_media_model import BaseMediaModel

class TVModel(BaseMediaModel):
    __tablename__ = 'tv_shows'
    name = Column(String, nullable=False)
    original_name = Column(String, nullable=True)
    first_air_date = Column(Date, nullable=True)
    origin_country = Column(String, nullable=True)