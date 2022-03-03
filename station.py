from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import database.models as models
from database.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title="Ronny the station chef",
    description="API to query baton detections on this station",
    version="6.9"
)


def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/detections/{last_id}')
def get_detections(last_id: int, db: Session = Depends(db)):
    detections: List[models.Detection] = db.query(models.Detection).filter(models.Detection.id > last_id).order_by(models.Detection.id).limit(1000).all()
    return detections
