from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# DATABASE_URL = "sqlite:///./ronny.db"

database_host = os.getenv("DATABASE_HOST", "localhost")
database_port = os.getenv("DATABASE_PORT", "5432")
database_user = os.getenv("DATABASE_USER", "ronny")
database_password = os.getenv("DATABASE_PASSWORD", "ronnydbpassword")
database_db = os.getenv("DATABASE_DB", "ronny")

DATABASE_URL = f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_db}"

extra_args = {'connect_args': {"check_same_thread": False}} if DATABASE_URL.startswith('sqlite') else {}

engine = create_engine(
    DATABASE_URL,
    **extra_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
