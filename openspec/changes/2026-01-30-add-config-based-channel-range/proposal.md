# Change: Add Config-Based Channel Range Scanning

## Why
Currently, the multimeter controller always scans all 16 channels (1-16) regardless of which channels are configured in the configuration file. This is inefficient when only a subset of channels is needed for testing. Users need the ability to scan only the channels defined in the configuration file, from the minimum to maximum channel numbers, to optimize scan time and reduce unnecessary measurements.

## What Changes
- Add logic to determine scan range based on configured channels (min to max channel numbers from config file)
- Modify `read_all_channels()` in `hardware/visa_interface.py` to use dynamic scan limits based on config
- Add method to get min/max channel numbers from `ConfigLoader`
- Update GUI to display unconfigured channels in gray color
- Maintain backward compatibility: if no config is loaded, scan all channels (1-16) as before
- Use existing SCPI commands `ROUT:LIMI:LOW` and `ROUT:LIMI:HIGH` to set scan range

## Impact
- Affected specs: multimeter-controller
- Affected code: 
  - `hardware/visa_interface.py` - modify scan logic to use config-based channel range
  - `config/config_loader.py` - add methods to get min/max channel numbers
  - `gui/widgets.py` - update channel indicator display to show unconfigured channels in gray
  - `gui/window.py` - integrate config-based scanning logic
