import logging
import re
from time import time
from typing import Optional

from sqlalchemy.orm import Session

from database.crud import get_detection_by_time_and_mac, create_detection
from database.database import SessionLocal, engine
from database.models import Base

logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

mac_regex = re.compile('(([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2})')
# We use the 5A:45:55:53:00 prefix to filter a bit in detections that are relevant for us.
# All our devices have this prefix
our_mac_regex = re.compile('(5A:45:55:53:00:[a-fA-F0-9]{2})')

logging.info("Setting up database")

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

try:
    while line := input():
        mac: Optional[re.Match] = mac_regex.search(line)
        our_mac: Optional[re.Match] = our_mac_regex.search(line)

        if mac:
            mac_address: str = mac.groups()[0]
            if our_mac:
                now = round(time())
                if get_detection_by_time_and_mac(db, now, mac_address):
                    logging.info("Skipping duplicate detection: %s", mac_address)
                else:
                    detection = create_detection(db, now, mac_address)
                    print(time(), detection)
                    logging.info("Detected a possible baton: %s", mac_address)
            else:
                logging.info("Ignoring detection with invalid mac: %s", mac_address)
        else:
            logging.warning("No mac detected in input: %s", line)
except EOFError:
    pass

logging.info("Closing database connection")
db.close()
