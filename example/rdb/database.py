from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABACE_URL = "postgres://user:password@localhost/dbname"
SQLALCHEMY_DATABACE_URL = "postgres://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABACE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
