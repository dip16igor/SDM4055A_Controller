# Change: Add Single Scan Button to Scan Control

## Why
Users need the ability to perform a one-time measurement scan without starting continuous polling. This is useful for taking spot measurements, checking values at specific moments, or when continuous scanning is not desired.

## What Changes
- Add a "Single Scan" button to the Scan Control section
- Implement single-shot scanning functionality that reads all channels once
- Keep existing "Start Scan" and "Stop Scan" buttons for continuous scanning
- Update UI state management to handle single scan button interactions

## Impact
- Affected specs: multimeter-controller
- Affected code: gui/window.py (UI layout and scan control logic)
