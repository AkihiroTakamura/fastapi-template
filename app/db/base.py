from app.db.base_class import Base, database  # noqa

# Import all the models, so that Base has them before Alembic execute

from app.models.item import Item  # noqa
from app.models.user import User  # noqa
