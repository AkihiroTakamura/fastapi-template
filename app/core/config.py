import logging
import sys
import secrets
from typing import List

from pydantic.networks import EmailStr
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

from app.core.logging import InterceptHandler


# Static Confinguration
API_PREFIX = "/api"
JWT_TOKEN_PREFIX = "Token"
VERSION = "0.0.0"


# Dynamic Configuration
# Read From environment variables or .env file
config = Config(".env")

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI Template")

DATABASE_URL: str = config("DB_CONNECTION", cast=str)
MAX_CONNECTIONS_COUNT: int = config(
    "MAX_CONNECTIONS_COUNT", cast=int, default=10
)
MIN_CONECTIONS_COUNT: int = config(
    "MIN_CONNECTIONS_COUNT", cast=int, default=10
)

SECRET_KEY: str = config(
    "SECRET_KEY", cast=str, default=secrets.token_urlsafe(32)
)

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)

DEBUG: bool = config("DEBUG", cast=bool, default=False)

FIRST_SUPERUSER: EmailStr = "admin@example.com"
FIRST_SUPERUSER_PASSWORD: str = "admin"

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

# Logging Configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
