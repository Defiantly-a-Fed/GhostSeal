<!---[![License: MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/justcallmekoko/ESP32Marauder/blob/master/LICENSE)--->
<!---[![Gitter](https://badges.gitter.im/justcallmekoko/ESP32Marauder.png)](https://gitter.im/justcallmekoko/ESP32Marauder)--->
<!---[![Build Status](https://travis-ci.com/justcallmekoko/ESP32Marauder.svg?branch=master)](https://travis-ci.com/justcallmekoko/ESP32Marauder)--->
<!---Shields/Badges https://shields.io/--->

# Ghost Seal

Ghost Seal is a policy-gated ESP32 Wi-Fi/BLE edge-control firmware developed for Project Spectrum Seals.

It is derived from ESP32 Marauder and currently focuses on safe UART-first operation, explicit capability authorization, controlled service execution, and future integration with Raspberry Pi-based Spectrum Seals nodes.

## Current Milestone

* Custom `ghostseal` CLI operational
* Firmware boots successfully
* Evil Portal startup is gated
* Explicit timed arming is required
* Automatic arm expiration works
* UART-first control branch established

## Safety Model

Ghost Seal boots in a disarmed state.

Capabilities that create access points, transmit, or perform other active operations must pass through Ghost Seal authorization controls before execution. Passive monitoring, device status, and diagnostics can remain available while disarmed.

## Current Commands

```text
ghostseal status
ghostseal arm <seconds>
ghostseal disarm
ghostseal ping
ghostseal version
ghostseal capabilities
```

## Project Status

Ghost Seal is under active development and is not yet production-ready.

The current development focus is:

1. Centralized capability authorization
2. UART command and response protocol
3. Raspberry Pi control integration
4. Telemetry and audit logging
5. Spectrum Seals console integration

## Attribution

Ghost Seal is derived from the ESP32 Marauder project created by Just Call Me Koko.

Original project:

```text
https://github.com/justcallmekoko/ESP32Marauder
```

Ghost Seal is an independent derivative project and is not an official ESP32 Marauder release.

## License

This project retains the original ESP32 Marauder MIT License and copyright notice.

Additional Ghost Seal modifications are copyright Gaby Strickland and are distributed under the same MIT License unless otherwise stated.

## Responsible Use

Ghost Seal is intended for authorized security testing, defensive research, education, and operation on systems and networks where the operator has permission.
