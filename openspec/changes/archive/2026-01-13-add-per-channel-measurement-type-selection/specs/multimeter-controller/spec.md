## ADDED Requirements

### Requirement: Per-Channel Measurement Type Selection
The system SHALL provide GUI controls to select measurement types for each individual channel before scanning.

#### Scenario: User selects DC Voltage for channel 1
- **WHEN** user selects "DC Voltage" from dropdown on channel 1 indicator
- **THEN** channel 1 is configured to measure DC voltage and selection is displayed

#### Scenario: User selects Resistance for channel 5
- **WHEN** user selects "Resistance" from dropdown on channel 5 indicator
- **THEN** channel 5 is configured to measure resistance and selection is displayed

#### Scenario: User selects different types for multiple channels
- **WHEN** user selects "DC Voltage" for channel 1, "AC Voltage" for channel 2, and "Resistance" for channel 3
- **THEN** all three channels are configured with their respective measurement types

#### Scenario: Measurement type selection persists
- **WHEN** user selects measurement type for a channel and performs multiple scans
- **THEN** selected measurement type is used for all subsequent scans until changed

#### Scenario: Invalid measurement type for channel
- **WHEN** user attempts to select current measurement on voltage-only channel (1-12)
- **THEN** selection is rejected and error message is displayed

### Requirement: Channel Configuration Before Scan
The system SHALL configure each channel with its selected measurement type before starting any scan operation.

#### Scenario: Configure channels before single scan
- **WHEN** user clicks "Single Scan" with different measurement types selected for channels
- **THEN** device is configured with all channel measurement types before scan executes

#### Scenario: Configure channels before continuous scan
- **WHEN** user clicks "Start Scan" with different measurement types selected for channels
- **THEN** device is configured with all channel measurement types before continuous scanning begins

#### Scenario: Channel configuration order
- **WHEN** device is being configured for scanning
- **THEN** channels are configured in sequential order (1-16) with their respective measurement types

### Requirement: Measurement Type Display
The system SHALL display the currently selected measurement type for each channel in the GUI.

#### Scenario: Display measurement type on channel indicator
- **WHEN** channel indicator is displayed
- **THEN** current measurement type is shown in a dropdown control or label

#### Scenario: Update display after selection change
- **WHEN** user changes measurement type selection for a channel
- **THEN** display immediately updates to show the new selection

#### Scenario: Show default measurement type
- **WHEN** application starts or channel is reset
- **THEN** default measurement type is displayed (DC Voltage for channels 1-12, DC Current for channels 13-16)

## MODIFIED Requirements

### Requirement: Multi-Channel Measurement Reading
The system SHALL read measurement data from multiple channels of the SDM4055A-SC multimeter with CS1016 scanning card at configurable intervals, using the measurement type configured for each channel.

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
