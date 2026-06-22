# Ghost Seal Node 1 Bridge

This directory contains the Node 1 Linux bridge code for Ghost Seal.

The bridge runs on the Raspberry Pi Zero 2 W sidecar and talks to the ESP32/Marauder console over USB serial or UART. It wraps command results in JSON, records an audit log, and keeps an explicit arm/disarm gate for transmit-capable commands.

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Basic checks

```bash
python3 ghostseal_bridge.py --port /dev/ttyACM0 status
python3 ghostseal_bridge.py --port /dev/ttyACM0 ping
python3 ghostseal_bridge.py --port /dev/ttyACM0 identify
python3 ghostseal_bridge.py --port /dev/ttyACM0 info
```

## Passive tools

```bash
python3 ghostseal_bridge.py tool list
python3 ghostseal_bridge.py --port /dev/ttyACM0 tool start packet_rate
python3 ghostseal_bridge.py --port /dev/ttyACM0 stop
```

## Active gate

Transmit-capable commands are blocked unless the local operator explicitly opens the active gate.

```bash
python3 ghostseal_bridge.py arm 30
python3 ghostseal_bridge.py status
python3 ghostseal_bridge.py disarm
```

The bridge logs audit events to:

```text
~/ghostseal-node1/logs/ghostseal_bridge_audit.jsonl
```

## Architecture

```text
Ghost Seal ESP32 / Marauder console
→ USB serial or UART
→ Node 1 Pi Zero bridge
→ JSON events / audit log
→ optional MQTT/core integration
```

## Notes

This bridge preserves a route to Marauder console commands while adding policy, JSON output, and audit logging around the command path.
