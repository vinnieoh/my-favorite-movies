from typing import ClassVar
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings
from dotenv import dotenv_values

class Settings(BaseSettings):
    _config_env = dotenv_values("./dotenv_files/.env")

    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = "My Favorite Movies"
    API_MOVIE: str = _config_env.get("API_MOVIE", "default_api_movie_url")
    DB_URL: str = _config_env.get("DB_URL", "default_database_url")
    DBBaseModel: ClassVar = declarative_base() 

    # Configurações para JWT
    JWT_SECRET: str = _config_env.get("JWT_SECRET", "default_jwt_secret")
    ALGORITHM: str = _config_env.get("ALGORITHM", "HS256")

    # Configuração de expiração de token
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 semana
    
    class Config:
        case_sensitive = True

settings: Settings = Settings()
