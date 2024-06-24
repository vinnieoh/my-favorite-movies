from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from uuid import UUID

class CommentBaseSchema(BaseModel):
    user_id: UUID
    media_type: str  # Usar string simples ao invés de enum
    content: str
    media_id: int
    likes: Optional[int] = 0

    @validator('likes', pre=True)
    def validate_likes(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError('likes must be greater than or equal to 0')
        return v

    @validator('media_type')
    def validate_media_type(cls, v):
        if v not in ('movie', 'tv_show'):
            raise ValueError("media_type must be 'movie' or 'tv_show'")
        return v

    class Config:
        from_attributes = True

class CommentCreateSchema(CommentBaseSchema):
    pass

class CommentUpdateSchema(BaseModel):
    content: Optional[str]
    likes: Optional[int] = 0

    @validator('likes', pre=True)
    def validate_likes(cls, v):
        if v is None:
            return 0
        if v < 0:
            raise ValueError('likes must be greater than or equal to 0')
        return v

    class Config:
        from_attributes = True

class CommentResponseSchema(CommentBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
