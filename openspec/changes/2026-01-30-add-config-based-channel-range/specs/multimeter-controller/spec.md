## MODIFIED Requirements

### Requirement: Multi-Channel Measurement Reading
The system SHALL read measurement data from multiple channels of the SDM4055A-SC multimeter with CS1016 scanning card at configurable intervals, using the measurement type configured for each channel. When a configuration file is loaded, the system SHALL scan only the channels from the minimum to maximum channel numbers defined in the configuration. When no configuration file is loaded, the system SHALL scan all 16 channels (1-16).

#### Scenario: Read DC voltage measurement on channel configured for DC voltage
- **WHEN** device is connected and channel 1 is configured for DC voltage measurement
- **THEN** system reads DC voltage value from device and returns it as float

#### Scenario: Read AC voltage measurement on channel configured for AC voltage
- **WHEN** device is connected and channel 2 is configured for AC voltage measurement
- **THEN** system reads AC voltage value from device and returns it as float

#### Scenario: Read resistance measurement on channel configured for resistance
- **WHEN** device is connected and channel 3 is configured for resistance measurement
- **THEN** system reads resistance value from device and returns it as float

#### Scenario: Periodic polling with mixed measurement types
- **WHEN** device is connected and channels are configured with different measurement types
- **THEN** system reads each channel using its configured measurement type every 500ms and updates display

#### Scenario: Read during disconnection
- **WHEN** device is disconnected and polling timer attempts to read
- **THEN** system handles error gracefully and displays connection status

#### Scenario: Scan only configured channels when config is loaded
- **WHEN** configuration file is loaded with channels 1, 3, 5, and 13 configured
- **THEN** system sets scan limits from channel 1 (minimum) to channel 13 (maximum)
- **AND** only channels 1-13 are scanned during measurement operations
- **AND** channels 14-16 are not scanned

#### Scenario: Scan all channels when no config is loaded
- **WHEN** no configuration file is loaded
- **THEN** system sets scan limits from channel 1 to channel 16
- **AND** all 16 channels are scanned during measurement operations

#### Scenario: Scan with non-contiguous channel configuration
- **WHEN** configuration file is loaded with channels 2, 5, 10, and 15 configured
- **THEN** system sets scan limits from channel 2 (minimum) to channel 15 (maximum)
- **AND** channels 2-15 are scanned (including unconfigured channels in this range)
- **AND** channels 1 and 16 are not scanned

## ADDED Requirements

### Requirement: Unconfigured Channel Visual Indication
The system SHALL display unconfigured channels in gray color in the GUI to visually distinguish them from configured channels.

#### Scenario: Display unconfigured channels in gray
- **WHEN** configuration file is loaded with specific channels configured
- **THEN** channel indicators for unconfigured channels are displayed in gray color
- **AND** channel indicators for configured channels are displayed in normal color

#### Scenario: Reset channel colors when config is unloaded
- **WHEN** configuration file is unloaded
- **THEN** all channel indicators return to normal color
- **AND** no channels are displayed in gray

#### Scenario: Update channel colors on config load
- **WHEN** new configuration file is loaded
- **THEN** channel indicator colors are immediately updated to reflect new configuration
- **AND** previously configured channels that are now unconfigured turn gray
- **AND** previously unconfigured channels that are now configured return to normal color

### Requirement: Configuration Channel Range Query
The system SHALL provide methods to query the minimum and maximum channel numbers from the loaded configuration.

#### Scenario: Get minimum channel number from config
- **WHEN** configuration file is loaded with channels 3, 5, 7, and 10
- **THEN** `get_min_channel()` returns 3

#### Scenario: Get maximum channel number from config
- **WHEN** configuration file is loaded with channels 3, 5, 7, and 10
- **THEN** `get_max_channel()` returns 10

#### Scenario: Handle no configuration loaded
- **WHEN** no configuration file is loaded
- **THEN** `get_min_channel()` returns None
- **AND** `get_max_channel()` returns None

#### Scenario: Check if specific channel is configured
- **WHEN** configuration file is loaded with channels 1, 3, 5
- **THEN** `is_channel_configured(3)` returns True
- **AND** `is_channel_configured(4)` returns False
