# detector/sniffer.py

from scapy.all import sniff
from detector.scanner import analyze_packet
from utils.config import INTERFACE, CAPTURE_FILTER
from utils.logger import log_info

def start_sniffing():
    log_info(f"Sniffing started on interface: {INTERFACE}")
    sniff(iface=INTERFACE, filter=CAPTURE_FILTER, prn=analyze_packet, store=False)