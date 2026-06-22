# Node 1 Ragnar-Style Support

Node 1 is the Ghost Seal Wi-Fi/BLE command node for SPECTRUM SEALS.

It uses a Raspberry Pi Zero 2 W as a sidecar controller for the Ghost Seal ESP32 over UART.

## Validated Path

Operator -> ghostseal-node1 wrapper -> node1-agent.service -> ghostseal-bridge -> /dev/serial0 UART -> Ghost Seal ESP32 firmware

## Validated Commands

- ghostseal-node1 status
- ghostseal-node1 exec "help"
- ghostseal-node1 arm 60
- ghostseal-node1 disarm
- ghostseal-node1 tool list

## Runtime State Model

tx_permitted = armed / allowed

tx_active = module is actually active

This lets the Ragnar-style controller tell the difference between disarmed, armed-but-idle, active, and timed-out states.

## Evidence Captured

- node1_status.txt
- ghostseal_help.txt
- tool_list.txt

## Next Work

- Add command profiles
- Add friendly Node 1 aliases
- Expand command parity validation
- Add Node 1 remote storage and asset support
- Add future seals-core bridge
