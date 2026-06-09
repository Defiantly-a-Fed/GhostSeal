#!/usr/bin/env python3
"""
ghostseal-bridge v0.1.1

Node 1 command wrapper for Ghost Seal.

Purpose:
- Runs on Raspberry Pi Zero 2 W / Node 1.
- Auto-detects the ESP32 Ghost Seal serial port.
- Sends Ghost Seal native commands.
- Sends original Marauder commands through ghostseal exec.
- Logs all runtime output locally on the Pi.
- Keeps Ragnar from needing to directly fight over /dev/ttyACM0 later.

Usage:
  ghostseal-bridge ping
  ghostseal-bridge identify
  ghostseal-bridge status
  ghostseal-bridge arm <seconds>
  ghostseal-bridge disarm
  ghostseal-bridge info
  ghostseal-bridge stop

  ghostseal-bridge tool list
  ghostseal-bridge tool status
  ghostseal-bridge tool start <tool_name>
  ghostseal-bridge tool stop

  ghostseal-bridge exec <original Marauder command...>

Examples:
  ghostseal-bridge ping
  ghostseal-bridge arm 60
  ghostseal-bridge status
  ghostseal-bridge tool start packet_rate
  ghostseal-bridge tool stop
  ghostseal-bridge exec info
  ghostseal-bridge exec packetcount
  ghostseal-bridge stop
  ghostseal-bridge disarm
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import serial
from serial.tools import list_ports


BAUD = 115200

LOG_DIR = Path.home() / "ghostseal-node1" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def find_port() -> str:
    """
    Auto-detect the Ghost Seal ESP32 serial device.

    Common ESP32 serial paths:
    - /dev/ttyACM0
    - /dev/ttyUSB0

    /dev/ttyS0 is usually the Pi's hardware UART, so we avoid it.
    """
    ports = list(list_ports.comports())

    for port in ports:
        device = port.device

        if device.startswith("/dev/ttyACM") or device.startswith("/dev/ttyUSB"):
            return device

    raise RuntimeError("No Ghost Seal serial port found. Check USB cable and ESP32 power.")


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def parse_json(line: str):
    clean = line.strip()

    if not clean.startswith("{") or not clean.endswith("}"):
        return None

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        return None


def read_lines(ser, seconds: float, log):
    """
    Read and print serial lines for a short window.
    """
    end = time.time() + seconds
    lines = []

    while time.time() < end:
        if ser.in_waiting:
            raw = ser.readline()
            line = raw.decode("utf-8", errors="replace").strip()

            if line:
                print(line)
                log.write(line + "\n")

                event = parse_json(line)
                if event:
                    log.write(f"[parsed_event_type] {event.get('event_type', 'unknown')}\n")

                lines.append(line)
        else:
            time.sleep(0.05)

    log.flush()
    return lines


def send(command: str, read_time: float = 3.0):
    """
    Open serial, send one command, print/log response, then close serial.

    This is v0.1 behavior. Later v0.2 should become a persistent service so
    opening serial does not reset the ESP32 every command.
    """
    port = find_port()
    log_file = LOG_DIR / f"ghostseal_bridge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    print(f"[ghostseal-bridge] port={port} baud={BAUD}")
    print(f"[ghostseal-bridge] command={command}")
    print(f"[ghostseal-bridge] log={log_file}")

    with serial.Serial(port, BAUD, timeout=0.2) as ser, open(log_file, "a", encoding="utf-8") as log:
        time.sleep(1)

        log.write("============================================================\n")
        log.write("ghostseal-bridge v0.1.1\n")
        log.write(f"time={now()}\n")
        log.write(f"port={port}\n")
        log.write(f"baud={BAUD}\n")
        log.write(f"command={command}\n")
        log.write("============================================================\n")

        # Drain boot/idle text so the command response is easier to see.
        read_lines(ser, 0.75, log)

        print(f">>> {command}")
        log.write(f">>> {command}\n")

        ser.write((command + "\n").encode("utf-8"))
        ser.flush()

        return read_lines(ser, read_time, log)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Ghost Seal Node 1 serial bridge"
    )

    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("ping", help="Send ghostseal ping")
    sub.add_parser("identify", help="Send ghostseal identify")
    sub.add_parser("status", help="Send ghostseal status")
    sub.add_parser("info", help="Send ghostseal exec info")
    sub.add_parser("stop", help="Send stopscan")
    sub.add_parser("disarm", help="Send ghostseal disarm")

    arm_parser = sub.add_parser("arm", help="Arm Ghost Seal for N seconds")
    arm_parser.add_argument("seconds", type=int, help="Arm duration in seconds")

    tool_parser = sub.add_parser("tool", help="Ghost Seal passive tool commands")
    tool_sub = tool_parser.add_subparsers(dest="tool_cmd")

    tool_sub.add_parser("list", help="List Ghost Seal passive tools")
    tool_sub.add_parser("status", help="Show current Ghost Seal tool status")
    tool_sub.add_parser("stop", help="Stop current Ghost Seal tool")

    tool_start = tool_sub.add_parser("start", help="Start a Ghost Seal passive tool")
    tool_start.add_argument("tool_name", help="Tool name, ex: packet_rate")

    exec_parser = sub.add_parser("exec", help="Forward original Marauder command through ghostseal exec")
    exec_parser.add_argument("marauder_command", nargs=argparse.REMAINDER)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd == "ping":
        send("ghostseal ping", 2)

    elif args.cmd == "identify":
        send("ghostseal identify", 2)

    elif args.cmd == "status":
        send("ghostseal status", 2)

    elif args.cmd == "info":
        send("ghostseal exec info", 3)

    elif args.cmd == "stop":
        send("stopscan", 2)

    elif args.cmd == "disarm":
        send("ghostseal disarm", 2)

    elif args.cmd == "arm":
        if args.seconds < 1:
            print("ERROR: arm seconds must be at least 1")
            sys.exit(1)

        send(f"ghostseal arm {args.seconds}", 2)

    elif args.cmd == "tool":
        if args.tool_cmd == "list":
            send("ghostseal tool list", 3)

        elif args.tool_cmd == "status":
            send("ghostseal tool status", 2)

        elif args.tool_cmd == "stop":
            send("ghostseal tool stop", 2)

        elif args.tool_cmd == "start":
            send(f"ghostseal tool start {args.tool_name}", 3)

        else:
            print("ERROR: missing tool subcommand")
            print("Examples:")
            print("  ghostseal-bridge tool list")
            print("  ghostseal-bridge tool status")
            print("  ghostseal-bridge tool start packet_rate")
            print("  ghostseal-bridge tool stop")
            sys.exit(1)

    elif args.cmd == "exec":
        if not args.marauder_command:
            print("ERROR: missing Marauder command after exec")
            print("Example: ghostseal-bridge exec info")
            sys.exit(1)

        command = "ghostseal exec " + " ".join(args.marauder_command)
        send(command, 4)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
