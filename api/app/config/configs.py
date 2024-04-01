from pydantic import BaseSettings
#from sqlalchemy.ext.declarative import declarative_base
from pydantic import  BaseSettings
from dotenv import dotenv_values


class Settings(BaseSettings):
    config_env = dotenv_values(".env")
    
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = "My Favorite Movies"
    
    DB_URL: str = config_env["DB_URL"]
    #DBBaseModel = declarative_base()

    # Create new token in token_create.py
    JWT_SECRET: str = config_env["JWT_SECRET"]
    ALGORITHM: str = config_env["ALGORITHM"]

    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True

settings: Settings = Settings()