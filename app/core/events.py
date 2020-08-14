from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.db.events import connect_db, close_db


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        await close_db(app)

    return stop_app
