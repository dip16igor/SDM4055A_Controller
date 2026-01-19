# Change: Add Range-Based Unit Display

**Status: archived**

## Why
Currently, the system displays only base units (V, A, Ohm, F, Hz, C) regardless of the selected measurement range. The SDM4055A-SC multimeter supports multiple ranges for each measurement type (e.g., 200 mV, 2 V, 20 V for voltage), and users need to see the appropriate unit (mV, V, etc.) based on the selected range.

## What Changes
- Add range selection dropdown to ChannelIndicator widget
- Add range-to-unit mapping for each measurement type
- Update unit label automatically when range is changed
- Load and apply range values from configuration file
- Support range selection in configuration file format

## Impact
- Affected specs: multimeter-controller
- Affected code:
  - gui/widgets.py - ChannelIndicator class (add range dropdown and range-to-unit mapping)
  - config/config_loader.py - add range validation and parsing
  - gui/window.py - update configuration loading to handle ranges
