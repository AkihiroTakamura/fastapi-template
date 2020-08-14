from sqlalchemy.ext.declarative import declarative_base
import databases

from app.core.config import DATABASE_URL


Base = declarative_base()

database = databases.Database(DATABASE_URL)
