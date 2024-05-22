from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class TVBaseSchema(BaseModel):
    original_id: int
    original_language: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    genre_ids: Optional[str] = None
    backdrop_path: Optional[str] = None
    poster_path: Optional[str] = None
    is_adult: Optional[bool] = False
    name: str
    original_name: Optional[str] = None
    first_air_date: Optional[date] = None
    origin_country: Optional[str] = None
    
    class Config:
        from_attributes = True

class TVCreateSchema(TVBaseSchema):
    pass

class TVUpdateSchema(BaseModel):
    original_id: Optional[int] = None
    original_language: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    genre_ids: Optional[str] = None
    backdrop_path: Optional[str] = None
    poster_path: Optional[str] = None
    is_adult: Optional[bool] = False
    name: Optional[str] = None
    original_name: Optional[str] = None
    first_air_date: Optional[date] = None
    origin_country: Optional[str] = None
    user_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class TVResponseSchema(TVBaseSchema):
    id: UUID

    class Config:
        from_attributes = True
