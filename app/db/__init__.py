from .base_class import AlchemyBase  # noqa

# Import all the models, so that Base has them before Alembic execute
from app.models import *  # noqa
