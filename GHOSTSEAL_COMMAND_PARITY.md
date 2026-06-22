# Ghost Seal Command Parity

Ghost Seal is intended to preserve supported ESP32Marauder command capability while adding a controlled SPECTRUM SEALS command and validation layer.

## Goal

```text
ghostseal <native command>
ghostseal exec <original Marauder command>
```

The compatibility path should preserve original Marauder command access where the hardware supports it.

## Current validation source

Current validation is based on Node 1 bridge testing and should be re-run after every firmware change.

## Bridge basics

Validated bridge commands:

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

## Passive tools

Validated/tracked passive tools:

```text
packet_rate
channel_analyzer
channel_activity
signal_strength
ap_sta_scan
```

Expected stopped state:

```json
{
  "tool_armed": false,
  "tx_permitted": false,
  "tx_active": false,
  "remaining_ms": 0,
  "running": false,
  "scan_mode": 0
}
```

## Active command behavior

Transmit-capable commands require deliberate local operator action before forwarding.

Some commands require selected targets, list state, storage files, or configuration files before full behavior is visible.

## Next required work

```text
1. Commit the Node 1 bridge code.
2. Add Ghost Seal firmware source symbols inside esp32_marauder/.
3. Add a universal command route.
4. Re-run command parity tests from committed source.
5. Mark every command as validated, partial, blocked by config, or not tested.
```

## Completion rule

Ghost Seal is not complete until every supported command has a documented result and the source code implementing the Ghost Seal layer is visible in the repository.
