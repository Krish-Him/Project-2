import time
from collections import defaultdict
from utils.config import TIME_WINDOW, PORT_THRESHOLD
from utils.logger import log_warning
from defense.port_switcher import switch_port
from defense.firewall import block_ip

# Store packets per IP: [(timestamp, port), (timestamp, port)]
ip_data = defaultdict(list)

def analyze_packet(pkt):
    if not pkt.haslayer("IP"):
        return

    src_ip = pkt["IP"].src

    # Get destination port
    if pkt.haslayer("TCP"):
        dst_port = pkt["TCP"].dport
    elif pkt.haslayer("UDP"):
        dst_port = pkt["UDP"].dport
    else:
        return

    # Debug print to see packets
    print(f"Detected packet from {src_ip} to port {dst_port}")

    current_time = time.time()

    # Store packet time and port
    ip_data[src_ip].append((current_time, dst_port))

    # Keep only packets within TIME_WINDOW
    ip_data[src_ip] = [
        (t, p) for (t, p) in ip_data[src_ip]
        if current_time - t <= TIME_WINDOW
    ]

    # Count unique ports scanned in time window
    unique_ports = set(p for (t, p) in ip_data[src_ip])

    # Detection condition
    if len(unique_ports) >= PORT_THRESHOLD:
        log_warning(f"Port scan detected from {src_ip}")

        # Trigger defense
        switch_port()
        block_ip(src_ip)

        # Reset attacker data
        ip_data[src_ip] = []