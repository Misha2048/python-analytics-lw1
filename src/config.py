import os

from pydantic_settings import BaseSettings
from pydantic import Field


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    ELEMENT_AMOUNT: int = Field(default=20)
    ROWS: int = Field(default=4)
    COLS: int = Field(default=5)
    LOW: int = Field(default=0)
    HIGH: int = Field(default=20)

    LOG_LEVEL: str = Field(default="INFO")

    class Config:
        env_file: str = os.path.join(APP_ROOT, "../.env")
        env_file_encoding: str = 'utf-8'
        from_attributes: bool = True


settings: Settings = Settings()
