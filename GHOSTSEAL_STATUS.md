# Ghost Seal Status

Ghost Seal is the Node 1 command/control layer for the SPECTRUM SEALS project.

This repository is a fork of ESP32Marauder, so most of the visible code remains upstream firmware. The current working Ghost Seal code being added here is the Node 1 bridge layer.

## Current working layer

```text
Ghost Seal ESP32 / Marauder console
→ USB serial or UART
→ Node 1 bridge
→ JSON events and audit log
→ optional MQTT/core integration
```

## Added code

```text
node1_bridge/ghostseal_bridge.py
```

The bridge provides:

- serial port detection
- command forwarding
- JSON output
- audit logging
- passive tool mapping
- explicit arm/disarm state
- active-command blocking unless armed

## Validated bridge-level commands

```text
ping
identify
status
info
arm
disarm
stop
tool list
tool status
tool start
exec
```

## Passive tools tracked by the bridge

```text
packet_rate
channel_analyzer
channel_activity
signal_strength
ap_sta_scan
```

## Active command control model

Ghost Seal separates commands into two classes:

```text
standard/passive commands
active/transmit-capable commands
```

Passive commands may run without opening the active gate.

Transmit-capable commands require explicit local operator arming before forwarding.

## Next required cleanup

```text
1. Commit the Node 1 bridge directory.
2. Add firmware-level Ghost Seal symbols inside esp32_marauder/.
3. Add a universal ghostseal exec route in firmware.
4. Keep command parity tracking updated.
5. Re-run validation from committed source.
```

## Current honest status

```text
Node 1 bridge code is present.
Firmware fork cleanup is still in progress.
```
