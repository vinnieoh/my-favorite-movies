from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
import uuid

class UsuarioSchemaBase(BaseModel):
    firstName: str
    lastName: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: lambda v: str(v),  # Codifica UUIDs como strings
        }

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str
    
    
class UsuarioSchemaUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: lambda v: str(v),  # Codifica UUIDs como strings
        }

class UsuarioIdSchemas(UsuarioSchemaBase):
    id: Optional[UUID4]  # Troque Optional[str] por UUID4 para correta tipagem

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: lambda v: str(v),  # Codifica UUIDs como strings
        }


class UsuarioSchemaEmail(UsuarioIdSchemas):
    email: EmailStr
