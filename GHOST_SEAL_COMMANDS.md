# Ghost Seal Command Reference

> **Development status:** Universal Marauder command forwarding is implemented through `ghostseal exec <original Marauder command>`. Command parity is still being validated feature-by-feature. Commands marked **Validated** have been hardware-tested on the current Ghost Seal build.

## Safety and authorization model

Ghost Seal starts disarmed. Transmit-capable commands must be denied unless the operator explicitly arms the device for a limited time.

```text
ghostseal arm <seconds>
ghostseal disarm
```

Always use Ghost Seal only on hardware, networks, and radio environments you own or are authorized to test.

## Native Ghost Seal commands

| Command | Purpose | Status |
|---|---|---|
| `ghostseal` | Show Ghost Seal help JSON | Validated |
| `ghostseal ping` | Verify UART control path | Validated |
| `ghostseal identify` | Return device identity JSON | Validated |
| `ghostseal status` | Show authorization and tool state | Validated |
| `ghostseal arm <sec>` | Temporarily permit active operations | Validated |
| `ghostseal disarm` | Disable transmission and stop current scan | Validated |
| `ghostseal exec <command>` | Forward an original Marauder command | Validated |
| `ghostseal tool list` | List registered passive tools | Validated |
| `ghostseal tool status` | Show current tool/scan state | Validated |
| `ghostseal tool start <tool>` | Start a registered passive tool | Validated |
| `ghostseal tool stop` | Stop the current registered tool | Validated |

### Registered passive tools

| Tool | Underlying mode | Status |
|---|---:|---|
| `packet_rate` | `WIFI_SCAN_PACKET_RATE` / mode 48 | Validated |
| `channel_analyzer` | `WIFI_SCAN_CHAN_ANALYZER` / mode 46 | Validated |
| `channel_activity` | `WIFI_SCAN_CHAN_ACT` | Validated |
| `signal_strength` | `WIFI_SCAN_SIG_STREN` | Validated |
| `ap_sta_scan` | `WIFI_SCAN_AP_STA` | Validated |

## Universal forwarding

Original Marauder commands are called through:

```text
ghostseal exec <original Marauder command>
```

Example:

```text
ghostseal exec info
ghostseal exec scanall
stopscan
```

Recursive forwarding is blocked:

```text
ghostseal exec ghostseal status
```

## Administrative and device commands

| Forwarded command | Purpose | Validation |
|---|---|---|
| `help` | Show original Marauder CLI help | Validated |
| `info` | Show device/firmware information | Validated |
| `channel [-s <channel>]` | View or set Wi-Fi channel | Pending |
| `settings ...` | View or change settings | Pending |
| `clearlist -a/-c/-s` | Clear stored AP/client/SSID lists | Pending |
| `reboot` | Restart device | Pending |
| `update -s/-w` | Firmware update path | Hardware-dependent |
| `ls <directory>` | List SD-card directory | Hardware-dependent |
| `led ...` | Control supported LED | Hardware-dependent |
| `brightness ...` | View/change supported display brightness | Hardware-dependent |
| `stopscan` | Stop current scan/operation | Validated |

## Passive Wi-Fi observation commands

| Forwarded command | Purpose | Validation |
|---|---|---|
| `scanall` | Scan access points and stations | Validated |
| `packetcount` | Show packet-rate activity | Validated |
| `sigmon` | Signal-strength monitor | Pending |
| `sniffraw` | Raw Wi-Fi capture | Pending |
| `sniffbeacon` | Observe beacon frames | Validated |
| `sniffprobe` | Observe probe requests | Pending |
| `sniffdeauth` | Observe deauthentication frames | Pending |
| `sniffpmkid` | PMKID/EAPOL observation path | Pending |
| `sniffsae` | SAE commit observation | Pending |
| `sniffpwn` | Pwnagotchi observation | Pending |
| `sniffpinescan` | PineScan observation | Pending |
| `sniffmultissid` | Multi-SSID observation | Pending |
| `mactrack` | Track selected MAC activity | Pending |
| `wardrive` | GPS-assisted Wi-Fi logging | Hardware-dependent |
| `wardrivepoi <label>` | Tag a wardrive point of interest | Hardware-dependent |

## Wi-Fi list and configuration commands

| Forwarded command | Purpose | Validation |
|---|---|---|
| `list -a/-c/-s/-t/-i/-p` | List discovered or stored entries | Pending |
| `select ...` | Select APs, clients, or SSIDs | Pending |
| `ssid ...` | Add/remove SSID entries | Pending |
| `add ...` | Manually add AP/client entries | Pending |
| `save -a/-s` | Save AP or SSID lists | Hardware-dependent |
| `load -a/-s` | Load AP or SSID lists | Hardware-dependent |
| `randapmac` | Generate random AP MAC | Pending |
| `randstamac` | Generate random station MAC | Pending |
| `cloneapmac` | Clone selected AP MAC | Pending |
| `clonestamac` | Clone selected station MAC | Pending |

## Active Wi-Fi and network commands

These commands must be classified as active and denied while Ghost Seal is disarmed.

| Forwarded command | Purpose | Gate validation |
|---|---|---|
| `evilportal -c start ...` | Start Evil Portal path | Validated |
| `karma ...` | Karma/Evil Portal path | Pending |
| `attack ...` | Original Marauder Wi-Fi attack dispatcher | Pending |
| `join ...` | Join an authorized Wi-Fi network | Pending |
| `pingscan` | Active network discovery | Pending |
| `arpscan` | Active ARP discovery | Pending |
| `portscan` | Active port discovery | Pending |
| `sniffpmkid -d ...` | Active PMKID path with deauth option | Pending |

Known original `attack -t` types exposed by the fork include:

```text
deauth, beacon, probe, rickroll, funny, badmsg, sleep, sae, csa, quiet
```

## Bluetooth commands

Bluetooth functionality requires a compatible NimBLE-Arduino dependency and a build with `HAS_BT` enabled.

| Forwarded command | Purpose | Validation |
|---|---|---|
| `sniffbt` | General BLE observation | Build/runtime validation pending |
| `sniffbt -t airtag` | AirTag observation | Pending |
| `sniffbt -t flipper` | Flipper BLE observation | Pending |
| `sniffbt -t flock` | Flock-device observation | Pending |
| `sniffbt -t meta` | Meta-device observation | Pending |
| `sniffskim` | BLE skimmer observation | Pending |
| `spoofat ...` | AirTag spoofing path | Active; pending |
| `blespam -t <type>` | BLE advertising test/spam dispatcher | Active; pending |

Known `blespam -t` types exposed by the fork include:

```text
sourapple, applejuice, windows, samsung, google, flipper, all
```

## GPS commands

| Forwarded command | Purpose | Validation |
|---|---|---|
| `gpsdata` | Stream GPS data | Hardware-dependent |
| `gps ...` | Query/configure GPS information | Hardware-dependent |
| `nmea` | Stream NMEA data | Hardware-dependent |
| `gpspoi -s/-m/-e` | GPS point-of-interest workflow | Hardware-dependent |
| `gpstracker` | GPS tracking path | Hardware-dependent |

## Current validated milestone

Validated on the `ghostseal-command-parity` branch:

```text
Ghost Seal help, ping, identify, status
arm, timeout, disarm
ghostseal exec help
ghostseal exec info
ghostseal exec packetcount
ghostseal exec sniffbeacon
recursive forwarding protection
passive tool registry start/status/stop
stopscan
disarm stopping the current scan
Evil Portal denied while disarmed
Evil Portal permitted while briefly armed
active Wi-Fi transmission path
```

## Completion criteria

Ghost Seal command parity is complete only when every supported original Marauder command:

1. Can be reached through `ghostseal exec`.
2. Preserves its original behavior.
3. Produces usable UART output.
4. Enforces Ghost Seal authorization for transmit-capable operations.
5. Has a recorded hardware test result.
