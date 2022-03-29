from datetime import datetime
import random
import time

from database.models import Base, Detection
from database.database import SessionLocal, engine

from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

test_mac_prefix = "ba:db:ee:f0:00"


while True:
    random_mac = f'{test_mac_prefix}:{random.randrange(256):02x}'
    random_rssi = -random.randrange(50, 90)
    random_baton_uptime_ms = random.randrange(1000_000)
    random_battery_percentage = random.uniform(10, 95)
    detection: Detection = Detection(
        detection_time=datetime.now(),
        mac=random_mac,
        rssi=random_rssi,
        baton_uptime_ms=random_baton_uptime_ms,
        battery_percentage=random_battery_percentage,
    )
    db.add(detection)
    db.commit()
    print(detection)
    time.sleep(random.uniform(1, 2))
    
