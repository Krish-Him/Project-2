# defense/port_switcher.py

import random
import os
from utils.config import PORT_RANGE_START, PORT_RANGE_END, INTERNAL_SERVICE_PORT
from utils.logger import log_info

def switch_port():
    new_port = random.randint(PORT_RANGE_START, PORT_RANGE_END)

    # Flush old NAT rules
    os.system("iptables -t nat -F")

    # Add new rule
    cmd = f"iptables -t nat -A PREROUTING -p tcp --dport {new_port} -j REDIRECT --to-port {INTERNAL_SERVICE_PORT}"
    os.system(cmd)

    log_info(f"Port switched to {new_port}")