# Ghost Seal Safety Model

Ghost Seal is designed to operate safely on networks by restricting active capabilities unless explicitly authorised.  The key aspects of the safety model are:

1. **Disarmed by default:** On every boot, Ghost Seal starts in a disarmed state and disables Wi‑Fi access point creation and other active radio functions.
2. **Explicit arming:** To enable active capabilities, the controller must issue `ghostseal arm <seconds>`.  This sets an expiration timer and authorises certain services (e.g. Evil Portal) until the timer expires.
3. **Automatic disarming:** When the arm timer expires, Ghost Seal automatically disarms and stops any running gated services.  Operators can also issue `ghostseal disarm` to immediately end the authorised period.
4. **Centralised gating:** A common authorisation function checks whether a capability is permitted before it runs.  This prevents scattered checks and ensures consistent enforcement across services.
5. **Passive functions unaffected:** Passive scanning, telemetry, version reporting and other read‑only diagnostics are available even when disarmed.  Only active transmissions or AP creation are gated.

This model aims to prevent accidental or unauthorised activation of potentially disruptive capabilities.
