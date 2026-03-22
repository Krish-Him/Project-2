from scapy.all import sniff, conf
from detector.scanner import analyze_packet
from utils.config import CAPTURE_FILTER, INTERFACES
from utils.logger import log_info
import threading

def sniff_interface(interface):
    log_info(f"Sniffing started on interface: {interface}")
    sniff(iface=interface, filter=CAPTURE_FILTER, prn=analyze_packet, store=False)

def start_sniffing():
    conf.use_pcap = True

    threads = []

    for interface in INTERFACES:
        t = threading.Thread(target=sniff_interface, args=(interface,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()