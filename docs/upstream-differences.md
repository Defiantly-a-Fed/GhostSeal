Differences from ESP32 Marauder

Ghost Seal currently differs from the upstream ESP32 Marauder project in several key areas:

* **Custom CLI:** Ghost Seal implements a `ghostseal` command-line interface replacing or supplementing the original Marauder commands. Commands are designed for machine parseability and controlled gating.
* **Timed authorization:** Active capabilities require an `arm <seconds>` command. The device automatically returns to a disarmed state when the timer expires or when disarmed manually.
* **Centralized gating:** A single authorization function controls access to active services, such as Evil Portal, active Wi-Fi transmit and BLE. Passive scanning and other diagnostic functions remain available in the disarmed state.
* **UART-first control:** The primary control transport is USB/UART, enabling integration with a Raspberry Pi or other controller. Wi-Fi access point creation is disabled by default until authorized.
* **Future integration:** Work is underway to integrate with the Spectrum Seals console via Raspberry Pi and to provide telemetry, audit logging and MQTT reporting.
