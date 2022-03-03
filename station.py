from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from socket import gethostname

import database.crud as crud
import database.models as models
import database.schemas as schemas
from database.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title="Ronny the station chef",
    description="API to query baton detections on this station",
    version="6.9"
)

station_id: str = gethostname()


def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/detections/{last_id}', response_model=schemas.DetectionsResponse)
def get_detections(last_id: int, limit: int = 1000, database: Session = Depends(db)):
    return schemas.DetectionsResponse(
        detections=crud.get_detections_after(database, last_id, limit=limit),
        station_id=station_id
    )
