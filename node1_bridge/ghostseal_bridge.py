#!/usr/bin/env python3
"""
Ghost Seal Node 1 bridge.

A local Linux bridge for commanding an ESP32 Marauder/Ghost Seal console over
USB CDC or UART serial. The bridge wraps console traffic in machine-readable
JSON, records an audit log, and enforces an explicit arm/disarm gate before
forwarding transmit-capable commands.

This file is intended to run on the Node 1 Pi Zero 2 W sidecar.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import serial  # type: ignore
    import serial.tools.list_ports  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit("pyserial is required. Install with: python3 -m pip install pyserial") from exc

DEFAULT_BAUD = 115200
DEFAULT_TIMEOUT = 2.5
DEFAULT_STATE_PATH = Path.home() / ".ghostseal_bridge_state.json"
DEFAULT_AUDIT_PATH = Path.home() / "ghostseal-node1" / "logs" / "ghostseal_bridge_audit.jsonl"

PASSIVE_TOOL_MAP: dict[str, str] = {
    "packet_rate": "packetcount",
    "channel_analyzer": "sigmon",
    "channel_activity": "scanall",
    "signal_strength": "sigmon",
    "ap_sta_scan": "pingscan",
}

ACTIVE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^\s*attack\b",
        r"^\s*blespam\b",
        r"^\s*evilportal\s+.*\bstart\b",
        r"^\s*karma\b",
        r"^\s*join\b",
        r"^\s*ssid\s+-a\b",
        r"^\s*rand(ap|sta)mac\b",
        r"^\s*clone(ap|sta)mac\b",
    )
)

STOP_COMMANDS: tuple[str, ...] = ("stopscan", "stop")


@dataclass
class BridgeState:
    armed_until_epoch: float = 0.0
    last_port: str | None = None
    last_baud: int = DEFAULT_BAUD
    last_command: str | None = None
    last_command_epoch: float = 0.0

    @property
    def armed(self) -> bool:
        return time.time() < self.armed_until_epoch

    @property
    def remaining_ms(self) -> int:
        return max(0, int((self.armed_until_epoch - time.time()) * 1000))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_state(path: Path) -> BridgeState:
    if not path.exists():
        return BridgeState()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return BridgeState(**{k: v for k, v in data.items() if k in BridgeState.__annotations__})
    except Exception:
        return BridgeState()


def save_state(path: Path, state: BridgeState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")


def audit(path: Path, event_type: str, detail: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "timestamp_utc": utc_now(),
        "project": "SPECTRUM_SEALS",
        "node_id": "node1_ghostseal",
        "component": "ghostseal_bridge",
        "event_type": event_type,
        "detail": detail,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def is_active_command(command: str) -> bool:
    return any(pattern.search(command) for pattern in ACTIVE_PATTERNS)


def find_serial_port(preferred: str | None = None) -> str:
    if preferred:
        return preferred

    env_port = os.getenv("GHOSTSEAL_SERIAL")
    if env_port:
        return env_port

    candidates: list[str] = []
    for port in serial.tools.list_ports.comports():
        device = port.device
        text = f"{port.description} {port.manufacturer or ''} {port.hwid or ''}".lower()
        if any(token in text for token in ("usb", "uart", "cp210", "ch340", "esp32", "seeed", "xiao", "acm")):
            candidates.append(device)

    for common in ("/dev/ttyACM0", "/dev/ttyUSB0", "COM3", "COM4", "COM5"):
        if common in candidates or Path(common).exists():
            return common

    if candidates:
        return candidates[0]

    raise FileNotFoundError(
        "No serial port found. Use --port /dev/ttyACM0, --port /dev/ttyUSB0, or --port COMx."
    )


def read_available(ser: "serial.Serial", settle_seconds: float) -> str:
    deadline = time.time() + settle_seconds
    chunks: list[bytes] = []
    while time.time() < deadline:
        waiting = ser.in_waiting
        if waiting:
            chunks.append(ser.read(waiting))
            deadline = time.time() + 0.25
        else:
            time.sleep(0.05)
    return b"".join(chunks).decode("utf-8", errors="replace")


def send_console_command(port: str, baud: int, command: str, timeout: float) -> dict[str, Any]:
    started = time.time()
    with serial.Serial(port=port, baudrate=baud, timeout=0.15, write_timeout=1.0) as ser:
        time.sleep(0.10)
        banner = read_available(ser, 0.20)
        ser.write((command.rstrip("\r\n") + "\n").encode("utf-8"))
        ser.flush()
        output = read_available(ser, timeout)

    return {
        "ok": True,
        "port": port,
        "baud": baud,
        "command": command,
        "elapsed_ms": int((time.time() - started) * 1000),
        "banner": banner,
        "output": output,
    }


def json_print(obj: dict[str, Any]) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def bridge_response(ok: bool, event_type: str, detail: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": ok,
        "timestamp_utc": utc_now(),
        "project": "SPECTRUM_SEALS",
        "node_id": "node1_ghostseal",
        "component": "ghostseal_bridge",
        "event_type": event_type,
        **detail,
    }


def list_tools() -> dict[str, Any]:
    return bridge_response(
        True,
        "tool_list",
        {
            "tools": [
                {"name": name, "marauder_command": command, "policy": "passive"}
                for name, command in sorted(PASSIVE_TOOL_MAP.items())
            ]
        },
    )


def status_response(state: BridgeState, port: str | None) -> dict[str, Any]:
    return bridge_response(
        True,
        "bridge_status",
        {
            "armed": state.armed,
            "remaining_ms": state.remaining_ms,
            "last_port": state.last_port,
            "selected_port": port,
            "last_baud": state.last_baud,
            "last_command": state.last_command,
            "last_command_epoch": state.last_command_epoch,
            "active_gate": "open" if state.armed else "closed",
        },
    )


def run_forwarded(
    *,
    command: str,
    port: str | None,
    baud: int,
    timeout: float,
    state_path: Path,
    audit_path: Path,
    require_armed_for_active: bool,
) -> dict[str, Any]:
    state = load_state(state_path)
    active = is_active_command(command)

    if active and require_armed_for_active and not state.armed:
        response = bridge_response(
            False,
            "command_blocked",
            {
                "reason": "active_command_requires_arm",
                "policy": "active",
                "command": command,
                "armed": False,
            },
        )
        audit(audit_path, "command_blocked", response)
        return response

    selected_port = find_serial_port(port)
    state.last_port = selected_port
    state.last_baud = baud
    state.last_command = command
    state.last_command_epoch = time.time()
    save_state(state_path, state)

    try:
        result = send_console_command(selected_port, baud, command, timeout)
        response = bridge_response(
            True,
            "command_forwarded",
            {
                "policy": "active" if active else "passive",
                "armed": state.armed,
                "serial": result,
            },
        )
        audit(audit_path, "command_forwarded", response)
        return response
    except Exception as exc:
        response = bridge_response(
            False,
            "serial_error",
            {
                "command": command,
                "port": selected_port,
                "error": str(exc),
            },
        )
        audit(audit_path, "serial_error", response)
        return response


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ghost Seal Node 1 serial bridge")
    parser.add_argument("--port", default=None, help="Serial port, for example /dev/ttyACM0 or COM5")
    parser.add_argument("--baud", type=int, default=int(os.getenv("GHOSTSEAL_BAUD", DEFAULT_BAUD)))
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE_PATH)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT_PATH)
    parser.add_argument("--no-active-gate", action="store_true", help="Disable active command blocking for controlled local lab testing")

    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("ping")
    sub.add_parser("identify")
    sub.add_parser("status")
    sub.add_parser("info")
    sub.add_parser("disarm")
    sub.add_parser("stop")

    arm = sub.add_parser("arm")
    arm.add_argument("seconds", type=int, nargs="?", default=30)

    tool = sub.add_parser("tool")
    tool.add_argument("tool_action", choices=("list", "status", "start"))
    tool.add_argument("name", nargs="?")

    execute = sub.add_parser("exec")
    execute.add_argument("command", nargs=argparse.REMAINDER)

    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    state = load_state(args.state)

    if args.action == "arm":
        seconds = max(1, min(int(args.seconds), 300))
        state.armed_until_epoch = time.time() + seconds
        save_state(args.state, state)
        response = bridge_response(True, "active_gate_armed", {"seconds": seconds, "remaining_ms": state.remaining_ms})
        audit(args.audit, "active_gate_armed", response)
        json_print(response)
        return 0

    if args.action == "disarm":
        state.armed_until_epoch = 0.0
        save_state(args.state, state)
        response = bridge_response(True, "active_gate_disarmed", {"remaining_ms": 0})
        audit(args.audit, "active_gate_disarmed", response)
        json_print(response)
        return 0

    if args.action == "status":
        json_print(status_response(state, args.port))
        return 0

    if args.action == "tool":
        if args.tool_action == "list":
            json_print(list_tools())
            return 0
        if args.tool_action == "status":
            json_print(status_response(state, args.port))
            return 0
        if args.tool_action == "start":
            if not args.name or args.name not in PASSIVE_TOOL_MAP:
                json_print(bridge_response(False, "tool_error", {"error": "unknown_tool", "known_tools": sorted(PASSIVE_TOOL_MAP)}))
                return 2
            command = PASSIVE_TOOL_MAP[args.name]
            json_print(
                run_forwarded(
                    command=command,
                    port=args.port,
                    baud=args.baud,
                    timeout=args.timeout,
                    state_path=args.state,
                    audit_path=args.audit,
                    require_armed_for_active=not args.no_active_gate,
                )
            )
            return 0

    command_map = {
        "ping": "ping",
        "identify": "info",
        "info": "info",
        "stop": "stopscan",
    }

    if args.action == "exec":
        command = " ".join(args.command).strip()
        if not command:
            json_print(bridge_response(False, "command_error", {"error": "missing_exec_command"}))
            return 2
    else:
        command = command_map[args.action]

    response = run_forwarded(
        command=command,
        port=args.port,
        baud=args.baud,
        timeout=args.timeout,
        state_path=args.state,
        audit_path=args.audit,
        require_armed_for_active=not args.no_active_gate,
    )
    json_print(response)
    return 0 if response.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
