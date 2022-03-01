from pydantic import BaseModel


class DetectionBase(BaseModel):
    time: int
    mac: str


class DetectionCreate(DetectionBase):
    pass


class Detection(DetectionBase):
    id: int

    class Config:
        orm_mode = True
