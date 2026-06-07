<!---[![License: MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/justcallmekoko/ESP32Marauder/blob/master/LICENSE)--->
<!---[![Gitter](https://badges.gitter.im/justcallmekoko/ESP32Marauder.png)](https://gitter.im/justcallmekoko/ESP32Marauder)--->
<!---[![Build Status](https://travis-ci.com/justcallmekoko/ESP32Marauder.svg?branch=master)](https://travis-ci.com/justcallmekoko/ESP32Marauder)--->
<!---Shields/Badges https://shields.io/--->
Safety model

Ghost Seal separates command execution into two classes:

standard/passive commands
active/transmit-capable commands

Passive or standard commands may run without opening the active gate. Active commands must be explicitly armed using ghostseal-bridge arm <seconds> and then closed with ghostseal-bridge disarm. Cleanup is performed with ghostseal-bridge stop. The bridge has validated that active commands such as blespam, selected attack modes, and evilportal -c start are blocked while disarmed and only forwarded while armed.

ghostseal‑bridge commands

The Node 1 bridge provides a Linux command‑line interface to the Ghost Seal UART console. The general form is:

ghostseal-bridge <command>
Bridge command	Purpose	Example
ping	Check Ghost Seal response	ghostseal-bridge ping
identify	Return Ghost Seal identity JSON	ghostseal-bridge identify
status	Return arm/tool/scan status	ghostseal-bridge status
info	Forward Marauder info through Ghost Seal exec	ghostseal-bridge info
arm <seconds>	Open active gate for a limited time	ghostseal-bridge arm 30
disarm	Close active gate	ghostseal-bridge disarm
stop	Send stopscan cleanup command	ghostseal-bridge stop
tool list	List Ghost Seal passive tools	ghostseal-bridge tool list
tool status	Show passive tool state	ghostseal-bridge tool status
tool start <tool>	Start a Ghost Seal passive tool	ghostseal-bridge tool start packet_rate
exec <command>	Forward an original Marauder command through Ghost Seal	ghostseal-bridge exec \"info\"
Validated passive Ghost Seal tools

The following tools are currently exposed via ghostseal-bridge tool start <tool> and have been validated:

Passive tool	Observed scan mode	Validation status
packet_rate	48	PASS
channel_analyzer	46	PASS
channel_activity	71	PASS
signal_strength	29	PASS
ap_sta_scan	49	PASS

Expected final safe state after stopping a passive tool:

{
  "tool_armed": false,
  "tx_permitted": false,
  "tx_active": false,
  "remaining_ms": 0,
  "running": false,
  "scan_mode": 0
}
Validated active command behaviour

Active commands are tested only in a safe controlled environment. Each active command was executed using the pattern:

ghostseal-bridge disarm
ghostseal-bridge status

ghostseal-bridge arm 30
ghostseal-bridge exec "<active command>"
sleep 3
ghostseal-bridge status

ghostseal-bridge stop
ghostseal-bridge disarm
ghostseal-bridge status

Validated active commands include:

Active command	Result	Notes
evilportal -c start	PASS	Forwarded with policy=active, entered scan_mode=30, requires /ap.config.txt for full portal runtime
attack -t beacon	GATE PASS	Forwarded while armed; did not enter running mode from clean state; likely requires selected AP/SSID/list state
attack -t deauth	GATE PASS	Forwarded while armed; reported no selected targets
attack -t probe	GATE PASS	Forwarded while armed; reported no selected targets
attack -t rickroll	FULL PASS	Forwarded while armed; entered running state with scan_mode=9
blespam -t all	FULL PASS	Forwarded while armed; entered running state with scan_mode=38

Observed active scan modes:

Command	Observed scan mode
evilportal -c start	30
attack -t rickroll	9
blespam -t all	38
Forwarded Marauder command manifest

The Ghost Seal command parity goal is to keep all supported Marauder commands accessible through the Ghost Seal interface. The following commands are returned by ghostseal-bridge exec help:

    channel [-s <channel>]
    settings [-s <setting> enable/disable>]/[-r]
    clearlist -a/-c/-s
    reboot
    update -s/-w
    ls <directory>
    led -s <hex color>/-p <rainbow>
    gpsdata
    gps [-t] [-g] <fix/sat/lon/lat/alt/date/accuracy/text/nmea>
    [-n] <native/all/gps/glonass/galileo/navic/qzss/beidou>
    [-b = use BD vs GB for beidou]
    nmea
    gpspoi -s/-m/-e
    gpstracker -c <start/stop>
    evilportal [-c start [-w html.html]/sethtml <html.html>]
    karma -p <index>
    packetcount
    pingscan
    arpscan [-f]
    portscan [-a -t <ip index>]/[-s <ssh/telnet/dns/http/smtp/https/rdp>]
    sigmon
    scanall
    sniffraw
    sniffbeacon
    sniffprobe
    sniffpwn
    sniffpinescan
    sniffmultissid
    sniffdeauth
    sniffpmkid [-c <channel>][-d][-l]
    sniffsae
    stopscan [-f]
    mactrack
    attack -t <quiet/csa/sae/beacon [-l/-r/-a]/deauth [-c]/[-s <src mac>] [-d <dst mac>]/probe/rickroll/badmsg [-c]/sleep [-c]>
    info [-a <index>]
    list -s
    list -a
    list -c
    list -t
    list -i
    list -p
    select -a/-s/-c <index (comma separated)>/-f "equals <String> or contains <String>"
    ssid -a [-g <count>/-n <name>]
    ssid -r <index>
    save -a/-s
    load -a/-s
    join -a <index> -p <password>/-s
    randapmac
    randstamac
    cloneapmac [-a <index>]
    clonestamac [-s <index>]
    add -a -b <mac> [-ch <channel>] [-e <ssid>]
    add -c -b <mac> -ap <ap_index>
    sniffbt [-t] <airtag/flipper/flock/meta>
    blespam -t <sourapple/applejuice/google/samsung/windows/flipper/all>
    spoofat -t <index>
    sniffskim
    brightness [-c cycle] [-s <0-9>]
Recommended validation categories

The following table summarises the status of high‑level command categories. Each category lists example commands and the current validation status:

Category	Examples	Status
Bridge basics	ping, identify, status, info	Validated
Passive Ghost Seal tools	packet_rate, channel_analyzer, channel_activity, signal_strength, ap_sta_scan	Validated
Active gate blocking	blespam while disarmed	Validated
Active gate forwarding	evilportal, attack, blespam while armed	Partially validated
Target/config‑dependent commands	attack -t beacon, attack -t deauth, attack -t probe, evilportal sethtml	Needs target/config
Storage/config commands	ls, save, load, evilportal sethtml, GPS POI features	Not fully validated
GPS commands	gps, gpsdata, nmea, gpstracker	Not fully validated
Bluetooth commands	sniffbt, blespam, spoofat	Partially validated
Wi‑Fi sniffing commands	sniffraw, sniffbeacon, sniffprobe, etc.	Not fully validated
List/select commands	list, select, ssid, add	Not fully validated
Current known notes
First bridge connection after reconnect may include the ESP32/Marauder boot banner and partial startup UART output.
ghostseal-bridge stop currently forwards stopscan.
ghostseal-bridge tool stop packet_rate is not valid in v0.1.1; use ghostseal-bridge stop.
ap_sta_scan emits live raw scan output into the UART stream while running.
Bridge v0.1.1 currently mixes bridge metadata, command echo, raw Marauder output and Ghost Seal JSON events in terminal output.
Unknown forwarded commands currently return to prompt without a structured unknown_command JSON event.
evilportal -c start requires /ap.config.txt for full runtime.
Several attack commands require selected AP/client/list state before full runtime behaviour.
## License

This project retains the original ESP32 Marauder MIT License and copyright notice.

Additional Ghost Seal modifications are copyright Gaby Strickland and are distributed under the same MIT License unless otherwise stated.

## Responsible Use

Ghost Seal is intended for authorized security testing, defensive research, education, and operation on systems and networks where the operator has permission.
