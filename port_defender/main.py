# main.py

import sys
from detector.sniffer import start_sniffing
from defense.port_switcher import switch_port
from utils.logger import log_info

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [start|switch-port|status]")
        return

    command = sys.argv[1]

    if command == "start":
        log_info("Starting Port Defender...")
        start_sniffing()

    elif command == "switch-port":
        switch_port()

    elif command == "status":
        log_info("System is running...")

    else:
        print("Invalid command")

if __name__ == "__main__":
    main()