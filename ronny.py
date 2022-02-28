import logging

from models import Detection, database_setup, database_cleanup

from time import time
import re
from typing import Optional
import logging

logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

mac_regex = re.compile('(([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2})')
# We use the F4:C8:5E prefix to filter a bit in detections that are relevant for us.
# All our devices have this prefix
our_mac_regex = re.compile('(F4:C8:5E:([a-fA-F0-9]{2}:){2}[a-fA-F0-9]{2})')

logging.info("Setting up database")
database_setup()

try:
    while line := input():
        mac: Optional[re.Match] = mac_regex.search(line)
        our_mac: Optional[re.Match] = our_mac_regex.search(line)

        if mac:
            mac_address: str = mac.groups()[0]
            if our_mac:
                now = time()
                if Detection.get_or_none(Detection.time == now, Detection.mac == mac_address):
                    logging.info("Skipping duplicate detection: %s", mac_address)
                else:
                    Detection.get_or_create(
                        time=now,
                        mac=mac_address
                    )
                    logging.info("Detected a possible baton: %s", mac_address)
            else:
                logging.info("Ignoring detection with invalid mac: %s", mac_address)
        else:
            logging.warning("No mac detected in input: %s", line)
except EOFError:
    pass

logging.info("Closing database connection")
database_cleanup()
