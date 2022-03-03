from typing import List, Optional

from sqlalchemy.orm import Session

from .models import Detection


def get_detections(db: Session) -> List[Detection]:
    return db.query(Detection).all()


def get_detections_after(db: Session, from_id: int) -> List[Detection]:
    return db.query(Detection).filter(Detection.id > from_id).all()


def get_detection_by_time_and_mac(db: Session, time: int, mac: str) -> Optional[Detection]:
    return db.query(Detection).filter(Detection.time == time, Detection.mac == mac).one_or_none()
