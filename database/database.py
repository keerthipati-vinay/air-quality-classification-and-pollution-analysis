import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

# LOAD ENV FILE

load_dotenv()

# DATABASE URL

DATABASE_URL = (

    f"postgresql://"

    f"{os.getenv('DB_USER')}:"

    f"{os.getenv('DB_PASSWORD')}@"

    f"{os.getenv('DB_HOST')}:"

    f"{os.getenv('DB_PORT')}/"

    f"{os.getenv('DB_NAME')}"
)

# ENGINE

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