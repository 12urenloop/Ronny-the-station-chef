from sqlalchemy import Column, String, Integer

from .database import Base


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(Integer, nullable=False)
    mac = Column(String, nullable=False)
