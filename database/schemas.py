from typing import List

from pydantic import BaseModel, Field


class Detection(BaseModel):
    id: int
    mac: str
    rssi: int
    baton_uptime_ms: int = Field(alias='uptime_ms')
    battery_percentage: float = Field(alias='battery')
    detection_time: int = Field(alias='detection_timestamp')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class DetectionsResponse(BaseModel):
    detections: List[Detection]
    station_id: str


class UnixTimeResponse(BaseModel):
    unix_time: int
