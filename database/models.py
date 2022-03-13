from sqlalchemy import Column, Integer, Float, CHAR
from sqlalchemy.types import DateTime, TIMESTAMP

from .database import Base


class Detection(Base):
    __tablename__ = "detection"
    id = Column(Integer, primary_key=True, index=True)
    detection_time = Column(TIMESTAMP, nullable=False)
    mac = Column(CHAR(6 * 2 + 5), nullable=False)
    rssi = Column(Integer, nullable=False)
    baton_uptime_ms = Column(Integer, nullable=False)
    battery_percentage = Column(Float, nullable=False)
