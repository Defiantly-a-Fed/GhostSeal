# Spectrum Seals UART Backbone Plan

## Rule

All field nodes must expose a UART control/data path to the Pi 5 core.

Network/HTTP control may be used for temporary development, but the final field architecture is UART-first.

## Core

Raspberry Pi 5 / seals-core

## Node 1

Raspberry Pi Zero 2 W / ghostseal-node1

Node 1 local link:

```text
Pi Zero 2 W -> USB serial / UART -> Ghost Seal ESP32
```

Node 1 core link:

```text
Pi 5 Core -> GPIO UART -> Pi Zero 2 W Node 1
```

## Confirmed UART status

### Pi 5

```text
UART console disabled
serial hardware enabled
/dev/serial0 present
```

### Node 1

```text
UART console disabled
enable_uart=1
/dev/serial0 -> ttyS0
```

## First UART link

```text
Pi 5 pin 8  / GPIO14 TXD -> Pi Zero pin 10 / GPIO15 RXD
Pi 5 pin 10 / GPIO15 RXD -> Pi Zero pin 8  / GPIO14 TXD
Pi 5 pin 6  / GND        -> Pi Zero pin 6  / GND
```

Do not connect 5V.
Do not connect 3.3V.
Power both Pis separately.

## Bench test plan

1. Wire TX/RX/GND only.
2. Power both Pis separately.
3. On Node 1, listen on `/dev/serial0`.
4. On Pi 5, send test text.
5. Reverse the direction.
6. If both directions work, build UART relay scripts.

## Future node map

```text
Core UART link 1 -> Node 1 / Ghost Seal sidecar
Core UART link 2 -> Node 2 / future sensor node
Core UART link 3 -> Node 3 / ADS-B node
Core UART link 4 -> Node 4 / SDR node
Core UART link 5 -> spare/debug
```

Exact future UART expansion method is still TBD because Pi 5 extra UART overlays need confirmation before pin assignment.

## Final assembly rule

Temporary jumper wires are only for bench testing.

Final assembly must use:
- labeled TX/RX/GND lines
- correct wire lengths
- strain relief
- removable connectors
- no wires over fans/heatsinks
- documented pin map
