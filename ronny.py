import struct
import time
import logging

from datatime import datetime

from database.models import Base, Detection
from database.database import SessionLocal, engine

from sqlalchemy.orm import Session
from scapy.layers.bluetooth import (
    HCI_LE_Meta_Advertising_Reports,
    EIR_Manufacturer_Specific_Data,
    BluetoothHCISocket,
    HCI_Hdr,
    HCI_Command_Hdr,
    HCI_Cmd_LE_Set_Scan_Parameters,
    HCI_Cmd_LE_Set_Scan_Enable,
)

logging.basicConfig(
    format="[%(levelname)s][%(asctime)s] %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

zeus_mac_prefix = "5a:45:55:53"


def packet_callback(packet):
    try:
        do_commit = False
        for report in packet[HCI_LE_Meta_Advertising_Reports].reports:
            if report.addr.startswith(zeus_mac_prefix):
                mac = str(report.addr).lower()
                if EIR_Manufacturer_Specific_Data not in packet:
                    logging.warning(f"No manufacturer information {mac}")
                    continue
                content = bytes(packet[EIR_Manufacturer_Specific_Data].payload)
                if len(content) == 23:
                    logging.warning(f"Skipping old baton {mac}")
                    continue
                elif len(content) != 9:
                    logging.error(f"Fake baton {mac} {len(content)} {content.hex()}")
                    continue
                uptime_ms, battery_percentage = struct.unpack(">QB", content)
                rssi = int(report.rssi)
                detection: Detection = Detection(
                    detection_time=datetime.fromtimestamp(time.time()),
                    mac=mac,
                    rssi=rssi,
                    baton_uptime_ms=uptime_ms,
                    battery_percentage=battery_percentage,
                )
                db.add(detection)
                do_commit = True
        if do_commit:
            db.commit()
    except Exception as e:
        logging.critical(e, exc_info=True)


bt = BluetoothHCISocket(0)
bt.sr(HCI_Hdr() / HCI_Command_Hdr() / HCI_Cmd_LE_Set_Scan_Parameters(type=0))
bt.sr(
    HCI_Hdr()
    / HCI_Command_Hdr()
    / HCI_Cmd_LE_Set_Scan_Enable(enable=True, filter_dups=False)
)
bt.sniff(
    lfilter=lambda p: HCI_LE_Meta_Advertising_Reports in p,
    store=False,
    prn=packet_callback,
)
