# Ghost Seal Command Reference

This document provides details on the commands available in the Ghost Seal CLI.  Each command returns a single‑line response prefaced by `GS:OK` on success or `GS:ERR` on error, with key‑value pairs for machine parsing.

## `ghostseal status`

Displays the current armed state, the remaining time before automatic disarm and whether gated services such as Evil Portal are active.

Example:

```
GS:OK command=status armed=false remaining=0 portal=false
```

## `ghostseal arm <seconds>`

Arms Ghost Seal for a specified number of seconds.  While armed, gated capabilities such as Evil Portal, active Wi‑Fi transmit and BLE are permitted.  After the specified time has elapsed, Ghost Seal automatically disarms.

Example:

```
ghostseal arm 60
GS:OK command=arm armed=true remaining=60
```

## `ghostseal disarm`

Immediately disarms Ghost Seal and stops any running gated services.  This resets the remaining time to zero.

Example:

```
GS:OK command=disarm armed=false remaining=0
```

## `ghostseal ping`

Returns a simple ping response to confirm communication with the device.

Example:

```
GS:OK command=ping response=pong
```

## `ghostseal version`

Reports the firmware version string.  Use this to verify the currently flashed build.

## `ghostseal capabilities`

Lists the active capabilities that are controlled by Ghost Seal, such as `EvilPortal`, `ActiveWifi`, `ActiveBle` and `RadioTransmit`.

## Error responses

When a gated command is attempted while disarmed, Ghost Seal returns an error response.  For example, if `evilportal -c start` is invoked when disarmed, Ghost Seal will output:

```
GS:ERR command=evilportal reason=not_armed
```
