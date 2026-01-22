# Change: Add Custom Name Field to Channel Configuration

## Why
Users need to assign custom names to measurement channels for easier identification and reporting. Currently, channels are only identified by their numeric IDs, which makes it difficult to understand what each channel measures in the context of the test setup.

## What Changes
- Add optional "Name" field to channel configuration CSV file
- Position Name field between "channel" and "measurement_type" columns
- Allow Name field to be empty (optional)
- Update CSV parser to handle whitespace in fields correctly
- Store custom channel names in memory for use during report generation
- Include custom names in report file headers when available

## Impact
- Affected specs: multimeter-controller
- Affected code: config/config_loader.py, report generation logic
