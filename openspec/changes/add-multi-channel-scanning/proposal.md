# Change: Add Multi-Channel Scanning with CS1016 Card

## Why
The current MVP implementation only supports single-channel measurements. The SDM4055A-SC multimeter with CS1016 scanning card can monitor up to 16 channels simultaneously. Adding multi-channel scanning capability will significantly enhance the utility of the application for automated testing, data logging, and multi-point monitoring scenarios.

## What Changes
- Implement multi-channel scanning support for CS1016 scanning card (16 channels total)
- Add channel configuration UI with measurement type selection per channel
- Create modern digital indicator widgets for all 16 channels with unit labels
- Implement START/STOP scanning controls with configurable scan interval (100ms-5s, default 1s)
- Add scan interval slider control
- Support measurement types for first 12 channels: DC/AC voltage, 2/4-wire resistance, capacitance, frequency, diode/continuity, RTD/thermocouple temperature
- Support AC/DC current measurement for last 4 channels
- Display USB device address and connection status at top of interface
- Update hardware abstraction layer to support multi-channel operations
- Add channel switching logic using CS1016 card commands

## Impact
- Affected specs: New capability `multi-channel-scanning`, MODIFIED `multimeter-controller`
- Affected code: [`gui/window.py`](gui/window.py), [`gui/widgets.py`](gui/widgets.py), [`hardware/visa_interface.py`](hardware/visa_interface.py), [`main.py`](main.py)
- Dependencies: No new dependencies required (existing PySide6, pyvisa sufficient)
