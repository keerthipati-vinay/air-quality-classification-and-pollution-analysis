from sqlalchemy import create_engine

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

DATABASE_URL=(
    "postgresql://postgres:"
    "vinay6789"
    "@localhost:5433/"
    "air_quality_db"
)

#engine 
engine = create_engine(
    DATABASE_URL
)

# SESSION

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# BASE CLASS

Base = declarative_base()

# DATABASE DEPENDENCY

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()