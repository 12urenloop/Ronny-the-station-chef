from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./ronny.db"
DATABASE_URL = "postgresql://ronny:ronnydbpassword@localhost/ronny"

extra_args = {'connect_args': {"check_same_thread": False}} if DATABASE_URL.startswith('sqlite') else {}

engine = create_engine(
    DATABASE_URL,
    **extra_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
