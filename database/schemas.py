from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator


class Detection(BaseModel):
    id: int
    mac: str
    rssi: int
    baton_uptime_ms: int = Field(alias="uptime_ms")
    battery_percentage: float = Field(alias="battery")
    detection_time: float = Field(alias="detection_timestamp")

    @validator("*", pre=True)
    def convert_time(cls, v) -> float:
        if isinstance(v, datetime):
            return v.timestamp()
        return v

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class DetectionsResponse(BaseModel):
    detections: List[Detection]
    station_id: str


class UnixTimeResponse(BaseModel):
    timestamp: int


class LastDetectionResponse(BaseModel):
    detection: Optional[Detection]
    station_id: str
