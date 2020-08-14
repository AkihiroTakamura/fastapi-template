from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import (
    ALLOWED_HOSTS,
    API_PREFIX,
    DEBUG,
    PROJECT_NAME,
    VERSION,
)

from app.api.routes import token
from app.api.api import router as api_router, tags_metadata
from app.api.depends import SessionLocal
from app.db.init_data import init_db

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    debug=DEBUG,
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = SessionLocal()
init_db(db=db)

app.include_router(token.router, tags=["oauth2"], prefix="/token")
app.include_router(api_router, prefix=API_PREFIX)
