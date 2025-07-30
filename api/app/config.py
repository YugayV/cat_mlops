import logging
import sys
from typing import List

from loguru import logger
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CatBoost MLOps API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    class Config:
        case_sensitive = True


def get_logger(logger_name: str = None):
    """Configure and return logger instance."""
    # Remove default handler
    logger.remove()
    
    # Add custom handler with format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # If logger_name is provided, you can use it for context
    if logger_name:
        logger.bind(name=logger_name)
    
    return logger


# Create settings instance
settings = Settings()