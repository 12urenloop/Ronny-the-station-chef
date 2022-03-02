from scapy.layers.bluetooth import *
import struct
from datetime import timedelta


zeus_mac_prefix = "5a:45:55:53"

def packet_callback(packet):
    for report in packet[HCI_LE_Meta_Advertising_Reports].reports:
        if report.addr.startswith(zeus_mac_prefix):
            content = bytes(packet[EIR_Manufacturer_Specific_Data])
            uptime_ms, battery_percentage = struct.unpack(">QB", content)
            uptime = timedelta(milliseconds=uptime_ms)
            print(report.addr)
            print(report.rssi)
            print(f"{battery_percentage}%")
            print(uptime)
            print("---")


bt = BluetoothHCISocket(0)
bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Parameters(type=0))
bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Enable(enable=True, filter_dups=False))
bt.sniff(lfilter=lambda p: HCI_LE_Meta_Advertising_Reports in p, store=False, prn=packet_callback)
