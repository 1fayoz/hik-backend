__all__ = (
    'BASE_DIR',
    'APP_SETTINGS',
)

import os
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


class EnvReader(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = "ignore"


class APPSettings(EnvReader):
    VERSION: str = '1.0.0'
    API_V1_PREFIX: str = "/api/v1"
    WS_PREFIX: str = "/ws"
    PROJECT_NAME: str = "FastAPI Boilerplate"
    MEDIA_URL: str = 'media/'
    STATIC_URL: str = 'static/'
    MEDIA_DIR: ClassVar[str] = os.path.join(BASE_DIR, 'media')
    STATIC_DIR: ClassVar[str] = os.path.join(BASE_DIR, 'static')
    TIME_ZONE: str = 'Asia/Tashkent'
    SERVER_HOST: str = 'localhost'
    DEBUG: bool = True


APP_SETTINGS = APPSettings()
