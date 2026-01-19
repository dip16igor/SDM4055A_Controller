# Change: Add Dynamic Unit Display Based on Measurement Type

**Status: archived**

## Why
Currently, the channel indicators display a static unit label (default "V") that does not update when the measurement type changes. This creates user confusion as the displayed unit may not match the actual measurement being taken (e.g., showing "V" when measuring current in Amperes). Users need clear, accurate unit labels that automatically reflect the selected measurement mode.

## What Changes
- Add automatic unit label updates when measurement type is changed manually via dropdown
- Add automatic unit label updates when configuration file is loaded
- Map measurement types to appropriate units:
  - Voltage measurements (VOLT:DC, VOLT:AC) → V
  - Current measurements (CURR:DC, CURR:AC) → A
  - Resistance measurements (RES, FRES) → Ω
  - Capacitance measurements (CAP) → F
  - Frequency measurements (FREQ) → Hz
  - Diode measurements (DIOD) → V
  - Continuity measurements (CONT) → Ω
  - Temperature measurements (TEMP:RTD, TEMP:THER) → °C
- Update ChannelIndicator widget to handle unit changes
- Ensure unit updates are triggered on both manual selection and config file load

## Impact
- Affected specs: multimeter-controller
- Affected code: 
  - gui/widgets.py - ChannelIndicator class
  - gui/window.py - _on_channel_measurement_type_changed and _apply_configuration methods
