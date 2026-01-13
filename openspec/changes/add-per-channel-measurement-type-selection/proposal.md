# Change: Add Per-Channel Measurement Type Selection

## Why
Currently, the system uses default measurement types for each channel (DC Voltage for channels 1-12, DC Current for channels 13-16) without allowing users to configure measurement types per channel through the GUI. Users need the ability to select different measurement types (DC Voltage, AC Voltage, Resistance, etc.) for each channel before scanning to match their specific measurement requirements.

## What Changes
- Add measurement type dropdown controls to each channel indicator in the GUI
- Store per-channel measurement type configurations in the GUI state
- Pass channel configurations to the scan manager before scanning starts
- Ensure device is configured with correct measurement types for each channel before scan execution
- Update channel indicators to display the currently selected measurement type

## Impact
- Affected specs: multimeter-controller
- Affected code: gui/window.py, gui/widgets.py, hardware/async_worker.py, hardware/visa_interface.py
