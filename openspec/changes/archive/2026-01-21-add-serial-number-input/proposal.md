# Change: Add Serial Number Input Field

## Why
The application needs a way for users to input and validate the serial number of the device being tested. This is important for tracking test results and ensuring proper identification of the tested product.

## What Changes
- Add a text input field for serial number entry in the "Scan Control" section
- Validate serial number format: PSN followed by exactly 9 digits (e.g., PSN123456789)
- Display invalid input in red color
- Display valid input in white color
- Hide the "Start Scan" and "Stop Scan" buttons (currently not used)

## Impact
- Affected specs: multimeter-controller
- Affected code: gui/window.py (Scan Control section)
