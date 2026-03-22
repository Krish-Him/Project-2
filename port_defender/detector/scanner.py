# detector/scanner.py

import time
from collections import defaultdict
from utils.config import TIME_WINDOW, PORT_THRESHOLD
from utils.logger import log_warning
from defense.port_switcher import switch_port
from defense.firewall import block_ip

# Track activity per IP
ip_data = defaultdict(lambda: {
    "ports": set(),
    "timestamps": []
})

def analyze_packet(pkt):
    if not pkt.haslayer("IP"):
        return

    src_ip = pkt["IP"].src

    if pkt.haslayer("TCP"):
        dst_port = pkt["TCP"].dport
    elif pkt.haslayer("UDP"):
        dst_port = pkt["UDP"].dport
    else:
        return

    current_time = time.time()

    # Update data
    ip_data[src_ip]["ports"].add(dst_port)
    ip_data[src_ip]["timestamps"].append(current_time)

    # Clean old timestamps
    ip_data[src_ip]["timestamps"] = [
        t for t in ip_data[src_ip]["timestamps"]
        if current_time - t <= TIME_WINDOW
    ]

    # Detection rule
    if len(ip_data[src_ip]["ports"]) > PORT_THRESHOLD:
        log_warning(f"Port scan detected from {src_ip}")

        # Trigger defense
        switch_port()
        block_ip(src_ip)

        # Reset attacker data
        ip_data[src_ip] = {"ports": set(), "timestamps": []}