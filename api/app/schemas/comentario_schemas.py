from pydantic import BaseModel, Field, conint, validator
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional
from uuid import UUID

# Enum for media types (TV or Movie)
class MediaType(PyEnum):
    MOVIE = "movie"
    TV_SHOW = "tv_show"

class CommentBaseSchema(BaseModel):
    user_id: UUID
    media_id: int
    media_type: MediaType
    content: str
    likes: Optional[int] = 0

    @validator('likes', pre=True, always=True)
    def validate_likes(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError('likes must be greater than or equal to 0')
        return v

    class Config:
        orm_mode = True
        use_enum_values = True  # Serialize enums as their values

class CommentCreateSchema(CommentBaseSchema):
    pass

class CommentUpdateSchema(BaseModel):
    content: Optional[str]
    likes: Optional[int] = 0

    @validator('likes', pre=True, always=True)
    def validate_likes(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError('likes must be greater than or equal to 0')
        return v

    class Config:
        orm_mode = True
        use_enum_values = True

class CommentResponseSchema(CommentBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
