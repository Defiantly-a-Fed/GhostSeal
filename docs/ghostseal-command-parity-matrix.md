# Ghost Seal Command Parity Matrix

This document tracks the status of each Marauder command as exposed through the Ghost Seal interface on the `ghostseal-command-parity` branch. The goal is command parity: every Marauder capability provided by the ESP32 hardware should remain reachable through Ghost Seal, subject to safety gating for transmit-capable commands.

## Status labels

- **PASS** – Command validated and working through Ghost Seal.
- **PARTIAL** – Command partially validated or requires further testing.
- **TARGET REQUIRED** – Command requires selecting a specific target or AP/STA from the scanning lists to operate.
- **CONFIG REQUIRED** – Command requires additional configuration or assets (e.g. EvilPortal HTML, GPS config).
- **TODO** – Not yet tested through Ghost Seal.
- **NOT SUPPORTED ON CURRENT HARDWARE** – Not applicable to this hardware or disabled for safety.

## Bridge basics

| Command | Status | Notes |
|---|---|---|
| ghostseal-bridge ping | PASS | Returns ping/pong; validated. |
| ghostseal-bridge identify | PASS | Returns Ghost Seal identity; validated. |
| ghostseal-bridge status | PASS | Returns state of active gate and passive tool; validated. |
| ghostseal-bridge info | PASS | Forwards Marauder `info`; validated. |
| ghostseal-bridge stop | PASS | Forwards `stopscan` to stop any running tool or attack. |
| ghostseal-bridge arm <seconds> | PASS | Opens active gate; validated with 30 s window. |
| ghostseal-bridge disarm | PASS | Closes active gate; validated. |

## Passive Ghost Seal tools

| Tool | Status | Scan mode | Notes |
|---|---|---|---|
| packet_rate | PASS | 48 | Logs packet rates; stops cleanly. |
| channel_analyzer | PASS | 46 | Reports channel noise data. |
| channel_activity | PASS | 71 | Reports channel usage; stops cleanly. |
| signal_strength | PASS | 29 | Reports signal strength; stops cleanly. |
| ap_sta_scan | PASS | 49 | Reports AP and STA scan results; outputs raw scan lines. |

## Active commands validated

| Command | Status | Notes |
|---|---|---|
| evilportal -c start | PARTIAL | Gate passes; enters scan_mode 30; requires /ap.config.txt to host portal. |
| attack -t beacon | TARGET REQUIRED | Gate passes but doesn't run without selecting an AP. |
| attack -t deauth | TARGET REQUIRED | Gate passes but requires target selection to send frames. |
| attack -t probe | TARGET REQUIRED | Gate passes but requires target selection. |
| attack -t rickroll | PASS | Gate passes; enters scan_mode 9 and transmits beacon spam. |
| blespam -t all | PASS | Gate passes; enters scan_mode 38 and transmits BLE spam. |

## Command manifest

The following is a list of Marauder commands from `help` output which require validation. Items not yet validated are tagged TODO.

| Command | Status | Notes |
|---|---|---|
| channel | TODO | Allows changing Wi-Fi channel; not yet tested through Ghost Seal. |
| settings | TODO | Modify or reset settings; not yet tested. |
| clearlist | TODO | Clear lists of APs, clients, or SSIDs. |
| reboot | TODO | Reboots the device. |
| update | TODO | Over-the-air update; not yet tested. |
| ls | TODO | List files; not yet tested. |
| led | TODO | Set LED colors; not yet tested. |
| gpsdata | TODO | Query GPS data; not yet tested. |
| gps | TODO | Request GPS fix or coordinates; not yet tested. |
| nmea | TODO | NMEA streaming; not yet tested. |
| gpspoi | TODO | GPS point-of-interest; not yet tested. |
| gpstracker | TODO | GPS tracking; not yet tested. |
| evilportal (sethtml, stop) | CONFIG REQUIRED | Requires HTML files to host; partial gating tested. |
| karma | TODO | Set Karma authentication type; not yet tested. |
| packetcount | TODO | Passive packet counting; not yet tested. |
| pingscan | TODO | Network scanning; not yet tested. |
| arpscan | TODO | ARP scanning; not yet tested. |
| portscan | TODO | Port scanning; not yet tested. |
| sigmon | TODO | Signal monitoring; not yet tested. |
| scanall | TODO | Combined scanning; not yet tested. |
| sniffraw | TODO | Raw packet sniffing; not yet tested. |
| sniffbeacon | TODO | Beacon sniffing; not yet tested. |
| sniffprobe | TODO | Probe request sniffing; not yet tested. |
| sniffpwn | TODO | Pineapple handshake sniff; not yet tested. |
| sniffpinescan | TODO | Pineapple scanning; not yet tested. |
| sniffmultissid | TODO | Multi-SSID sniffing; not yet tested. |
| sniffdeauth | TODO | Deauthentication sniffing; not yet tested. |
| sniffpmkid | TODO | PMKID sniffing; not yet tested. |
| sniffsae | TODO | SAE sniffing; not yet tested. |
| stopscan | PASS | Equivalent to ghostseal-bridge stop; stops scanning. |
| mactrack | TODO | Tracks MAC addresses; not yet tested. |
| attack (quiet, csa, sae, beacon, deauth, probe, rickroll, badmsg, sleep) | PARTIAL | Only beacon, deauth, probe, rickroll tested; others TBD. |
| info | PASS | Already validated via ghostseal-bridge info. |
| list (-s, -a, -c, -t, -i, -p) | TODO | Query lists; not yet tested. |
| select | TODO | Select AP or STA by index; not yet tested. |
| ssid | TODO | Add or remove SSIDs from transmit lists. |
| save, load | TODO | Save/restore lists; not yet tested. |
| join | TODO | Join a network; not yet tested. |
| randapmac | TODO | Randomize AP MAC; not yet tested. |
| randstamac | TODO | Randomize station MAC; not yet tested. |
| cloneapmac | TODO | Clone AP MAC address; not yet tested. |
| clonestamac | TODO | Clone station MAC; not yet tested. |
| add | TODO | Add a MAC/AP/SSID; not yet tested. |
| sniffbt | TODO | Bluetooth sniffing; not yet tested. |
| blespam -t <type> | PASS | Verified with `-t all` variant; other variants pending. |
| spoofat | TARGET REQUIRED | AirTag spoofing; requires target index. |
| sniffskim | TODO | Skimmer sniffing; not yet tested. |
| brightness | TODO | Adjust brightness; not yet tested. |

## Future work

- Validate remaining commands using the safe gating model. 
- Improve Ghost Seal bridging to capture structured JSON events and parse them on the host for easier monitoring.
- Document commands that are intentionally disabled or unsupported due to hardware limitations or legal concerns.
