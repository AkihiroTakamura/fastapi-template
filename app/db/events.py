import asyncpg
from fastapi import FastAPI
from loguru import logger

from app.core.config import (
    DATABASE_URL,
    MAX_CONNECTIONS_COUNT,
    MIN_CONECTIONS_COUNT,
)


async def connect_db(app: FastAPI) -> None:
    logger.info("Connecting to {0}", repr(DATABASE_URL))

    app.state.pool = await asyncpg.create_pool(
        str(DATABASE_URL),
        min_size=MIN_CONECTIONS_COUNT,
        max_size=MAX_CONNECTIONS_COUNT,
    )

    logger.info("Connection established")


async def close_db(app: FastAPI) -> None:
    logger.info("closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
