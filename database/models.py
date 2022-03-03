from sqlalchemy import Column, Integer, Float, CHAR
from sqlalchemy.schema import Index
from .database import Base


class Detection(Base):
    __tablename__ = 'detection'
    id = Column(Integer, primary_key=True, index=True)
    detection_time = Column(Integer, nullable=False)
    mac = Column(CHAR(6*2+5), nullable=False)
    rssi = Column(Integer, nullable=False)
    baton_uptime_ms = Column(Integer, nullable=False)
    battery_percentage = Column(Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'mac': self.mac,
            'rssi': self.rssi,
            'battery': self.battery_percentage,
            'uptime_ms': self.baton_uptime_ms,
            'detection_timestamp': self.detection_time
        }
