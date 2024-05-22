from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class MovieBaseSchema(BaseModel):
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
    title: str
    original_title: Optional[str] = None
    release_date: Optional[date] = None
    video: Optional[bool] = False

    class Config:
        from_attributes = True

class MovieCreateSchema(MovieBaseSchema):
    pass

class MovieUpdateSchema(BaseModel):
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
    title: Optional[str] = None
    original_title: Optional[str] = None
    release_date: Optional[date] = None
    video: Optional[bool] = False
    user_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class MovieResponseSchema(MovieBaseSchema):
    id: UUID

    class Config:
        from_attributes = True
