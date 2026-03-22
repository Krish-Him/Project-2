# defense/firewall.py

import os
from utils.config import BLOCK_ATTACKER
from utils.logger import log_info

def block_ip(ip):
    if not BLOCK_ATTACKER:
        return

    cmd = f"iptables -A INPUT -s {ip} -j DROP"
    os.system(cmd)

    log_info(f"Blocked IP: {ip}")