import time
from socket import gethostname

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import database.crud as crud
import database.models as models
import database.schemas as schemas
from database.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title="Ronny the station chef",
    description="API to query baton detections on this station",
    version="6.9",
)

station_id: str = gethostname()


def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/detections/{last_id}")
async def get_detections(
    last_id: int, limit: int = 1000, database: Session = Depends(db)
):
    '''Get all detections after last_id, so detection with id last_id not included'''
    return {
        'station_id': station_id,
        'detections': [d.serialize() for d in crud.get_detections_after(database, last_id, limit=limit)]
    }

@app.get("/time", response_model=schemas.UnixTimeResponse)
async def get_time():
    '''Get Unix timestamp in milliseconds, like `Date.now()` in JavaScript.'''
    return schemas.UnixTimeResponse(timestamp=int(time.time()*1000))


@app.get("/last_detection", response_model=schemas.LastDetectionResponse)
async def get_last_detection(database: Session = Depends(db)):
    '''Get the last detection. If there are no detections, `detection` will be null.'''
    return schemas.LastDetectionResponse(
        detection=crud.get_last_detection(database),
        station_id=station_id,
    )
