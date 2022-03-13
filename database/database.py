from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./ronny.db"
DATABASE_URL = "postgresql://postgres:postgres@localhost/ronny"

engine = create_engine(
    DATABASE_URL,
    # connect_args={"check_same_thread": False} # Only needed for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
