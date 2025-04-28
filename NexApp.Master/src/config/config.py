from pydantic_settings import BaseSettings
from src.utils import logger

class Settings(BaseSettings):
    try:
        DATABASE_URL: str
        SECRET_KEY: str
        ALGORITHM: str
        EXPIRE_TIME_MINUTES: int

        class Config:
            env_file = "src/.env"  # 👈 Pydantic will load variables from this
    except Exception as e:
        logger.logging_error(f"config erro : {str(e)}")

settings = Settings()

