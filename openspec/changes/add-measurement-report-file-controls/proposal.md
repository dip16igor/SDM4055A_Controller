# Change: Add Measurement Report File Controls

## Why
The application needs functionality to save measurement data to CSV files for later analysis and record keeping. Users should be able to either select an existing file or create a new report file with an automatically generated name based on the configuration file and current date.

## What Changes
- Add a "Select Report File" button in the "Scan Control" section to choose an existing CSV file for saving measurements
- Add a "New Report File" button in the "Scan Control" section to create a new CSV file with auto-generated name
- Auto-generated filename format: `<config_filename_without_extension>_<YYYY-MM-DD>.csv`
- Display the current report filename next to the buttons
- Store the selected report file path in the application state for later use

## Impact
- Affected specs: multimeter-controller
- Affected code: gui/window.py (Scan Control section)
