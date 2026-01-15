# Change: Add Channel Configuration File Loading

## Why
Users need an easy way to configure measurement settings for multiple channels without manually setting each channel in the UI. A configuration file allows:
- Quick setup of channel measurement types, ranges, and thresholds
- Easy editing in Excel or text editors
- Reusable configurations for different test scenarios
- Consistent threshold-based visual feedback for measurements

## What Changes
- Add CSV configuration file format for channel settings
- Create `ConfigLoader` module to parse and validate configuration files
- Add "Load Config" button to Scan Control section in main window
- Display loaded configuration file name in UI
- Implement threshold-based color coding for measurements:
  - Green: value within configured thresholds
  - Red: value outside configured thresholds
- Add threshold display to channel indicators showing configured thresholds
- Increase measurement value font size from 28pt to 36pt for better readability
- Support partial channel configuration (only configure channels you need)
- Add comprehensive validation for configuration files

## Impact
- Affected specs: multimeter-controller
- New files:
  - `config/config_loader.py` - Configuration parser module
  - `config/__init__.py` - Package initialization
  - `sample_config.csv` - Example configuration file
- Modified files:
  - `gui/window.py` - Add config loading UI and logic
  - `gui/widgets.py` - Add threshold support to ChannelIndicator

## Configuration File Format
CSV format with columns:
- `channel`: Channel number (1-16)
- `measurement_type`: Measurement type (VOLT:DC, VOLT:AC, RES, FRES, CAP, FREQ, DIOD, CONT, TEMP:RTD, TEMP:THER, CURR:DC, CURR:AC)
- `range`: Measurement range (AUTO or specific value)
- `lower_threshold`: Optional lower threshold for validation
- `upper_threshold`: Optional upper threshold for validation

Supports comment lines starting with `#` for documentation.
