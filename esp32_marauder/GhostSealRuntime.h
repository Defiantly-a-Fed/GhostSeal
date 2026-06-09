#pragma once

#include "Arduino.h"

class GhostSealRuntime {
  public:
    bool uartFirst = true;
    bool quietBoot = true;

    // Authorization state: active commands are allowed while true.
    bool toolArmed = false;

    // Runtime state: true only while a transmitting module is actually active.
    bool txEnabled = false;

    unsigned long armExpiresAt = 0;
    unsigned long armDurationMs = 0;

    void begin() {
      uartFirst = true;
      quietBoot = true;
      toolArmed = false;
      txEnabled = false;
      armExpiresAt = 0;
      armDurationMs = 0;
    }

    void arm(uint32_t durationSec) {
      if (durationSec < 1) durationSec = 1;
      if (durationSec > 300) durationSec = 300;

      toolArmed = true;
      txEnabled = false;

      armDurationMs = durationSec * 1000UL;
      armExpiresAt = millis() + armDurationMs;

      Serial.print(F(
        "{\"event_type\":\"ghostseal_tool_armed\","
        "\"duration_sec\":"
      ));
      Serial.print(durationSec);
      Serial.println(F(
        ",\"tx_permitted\":true,"
        "\"tx_active\":false}"
      ));
    }

    void disarm() {
      toolArmed = false;
      txEnabled = false;
      armExpiresAt = 0;
      armDurationMs = 0;

      Serial.println(F(
        "{\"event_type\":\"ghostseal_tool_disarmed\","
        "\"tx_permitted\":false,"
        "\"tx_active\":false}"
      ));
    }

    void checkTimeout() {
      if (
        toolArmed &&
        ((long)(millis() - armExpiresAt) >= 0)
      ) {
        disarm();
        Serial.println(F(
          "{\"event_type\":\"ghostseal_tool_timeout\"}"
        ));
      }
    }

    bool canTransmit(const char* moduleName) {
      checkTimeout();

      if (!toolArmed) {
        Serial.print(F(
          "{\"event_type\":\"ghostseal_cmd_blocked\","
          "\"module\":\""
        ));
        Serial.print(moduleName);
        Serial.println(F(
          "\",\"reason\":\"tool_not_armed\"}"
        ));
        return false;
      }

      return true;
    }

    void markTxStart(const char* moduleName) {
      if (!canTransmit(moduleName)) {
        return;
      }

      txEnabled = true;

      Serial.print(F(
        "{\"event_type\":\"ghostseal_tx_started\","
        "\"module\":\""
      ));
      Serial.print(moduleName);
      Serial.println(F("\"}"));
    }

    void markTxStop(const char* moduleName) {
      txEnabled = false;

      Serial.print(F(
        "{\"event_type\":\"ghostseal_tx_stopped\","
        "\"module\":\""
      ));
      Serial.print(moduleName);
      Serial.println(F("\"}"));
    }

    void status() {
      checkTimeout();

      Serial.print(F(
        "{\"event_type\":\"ghostseal_status\","
        "\"quiet_boot\":true,"
        "\"uart_first\":true,"
        "\"tool_armed\":"
      ));
      Serial.print(toolArmed ? F("true") : F("false"));

      Serial.print(F(",\"tx_permitted\":"));
      Serial.print(toolArmed ? F("true") : F("false"));

      Serial.print(F(",\"tx_active\":"));
      Serial.print(txEnabled ? F("true") : F("false"));

      Serial.print(F(",\"remaining_ms\":"));

      if (toolArmed && armExpiresAt > millis()) {
        Serial.print(armExpiresAt - millis());
      }
      else {
        Serial.print(0);
      }

      Serial.println(F("}"));
    }
};
extern GhostSealRuntime ghostseal_runtime;
