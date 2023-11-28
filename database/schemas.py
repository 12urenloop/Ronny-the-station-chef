from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field, field_serializer


class Detection(BaseModel):
    id: int
    mac: str
    rssi: int
    baton_uptime_ms: int = Field(alias="uptime_ms")
    battery_percentage: float = Field(alias="battery")
    detection_time: datetime = Field(alias="detection_timestamp")

    @field_serializer("detection_time")
    def convert_time(self, v: datetime, _info) -> float:
        return v.timestamp()

    class Config:
        from_attributes = True
        populate_by_name = True


class DetectionsResponse(BaseModel):
    detections: List[Detection]
    station_id: str


class UnixTimeResponse(BaseModel):
    timestamp: int


class LastDetectionResponse(BaseModel):
    detection: Optional[Detection]
    station_id: str
