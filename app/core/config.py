import logging
import sys
from typing import List

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler


# Static Confinguration
API_PREFIX = "/api"
JWT_TOKEN_PREFIX = "Token"
VERSION = "0.0.0"


# Dynamic Configuration
# Read From environment variables or .env file
config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI Template")

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)
MAX_CONNECTIONS_COUNT: int = config(
    "MAX_CONNECTIONS_COUNT", cast=int, default=10
)
MIN_CONECTIONS_COUNT: int = config(
    "MIN_CONNECTIONS_COUNT", cast=int, default=10
)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)

DEBUG: bool = config("DEBUG", cast=bool, default=False)


# Logging Configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])