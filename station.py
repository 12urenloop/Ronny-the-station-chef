from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import database.crud as crud
import database.models as models
import database.schemas as schemas
from database.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title="Ronny the station chef",
    description="Api to query baton detections on this station",
    version="6.9"
)


def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/detections/{last_id}', response_model=List[schemas.Detection])
def get_detections(last_id: int, db: Session = Depends(db)):
    detections: List[models.Detection] = crud.get_detections_after(db, last_id)
    return detections
