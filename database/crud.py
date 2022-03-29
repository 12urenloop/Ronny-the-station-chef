from typing import List

from sqlalchemy.orm import Session

from .models import Detection


def get_detections_after(
    db: Session, from_id: int, limit: int = 1000
) -> List[Detection]:
    return (
        db.query(Detection)
        .filter(Detection.id > from_id)
        .order_by(Detection.id)
        .limit(limit)
        .all()
    )
