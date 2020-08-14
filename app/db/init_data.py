from sqlalchemy.orm import Session

from app import service, schemas
from app.core import config


def init_db(db: Session) -> None:
    user = service.user.get_by_email(db, email=config.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = service.user.create(db, obj_in=user_in)
