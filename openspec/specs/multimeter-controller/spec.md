# Multimeter Controller

## Purpose
The Multimeter Controller provides a Python-based GUI application for communicating with and reading measurements from Siglent SDM4055A-SC 5½ digit digital multimeter via USB connection using VISA protocol. The controller supports single and multi-channel measurement modes with configurable measurement types per channel.
## Requirements
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
The system SHALL display currently selected measurement type for each channel in GUI.

#### Scenario: Display measurement type on channel indicator
- **WHEN** channel indicator is displayed
- **THEN** current measurement type is shown in a dropdown control or label

#### Scenario: Update display after selection change
- **WHEN** user changes measurement type selection for a channel
- **THEN** display immediately updates to show new selection

#### Scenario: Show default measurement type
- **WHEN** application starts or channel is reset
- **THEN** default measurement type is displayed (DC Voltage for channels 1-12, DC Current for channels 13-16)

### Requirement: Application Version System
The system SHALL provide a versioning system with version information stored in a separate file and displayed in the application header.

#### Scenario: Read version from file
- **WHEN** application starts
- **THEN** version information is read from version.py file

#### Scenario: Display version in application header
- **WHEN** application window is displayed
- **THEN** window title shows application name followed by version number (e.g., "SDM4055A Controller v1.0.0")

#### Scenario: Version format
- **WHEN** version is defined
- **THEN** version follows semantic versioning format (MAJOR.MINOR.PATCH, e.g., 1.0.0)

#### Scenario: Initial version
- **WHEN** version system is first implemented
- **THEN** initial version is set to 1.0.0

### Requirement: Serial Number Input Field
The system SHALL provide a text input field for entering the serial number of the device being tested in the "Scan Control" section of the GUI.

#### Scenario: Display serial number input field
- **WHEN** application window is displayed
- **THEN** serial number input field is visible in the "Scan Control" section

#### Scenario: Input field placement
- **WHEN** user views the "Scan Control" section
- **THEN** serial number input field is positioned before the "Single Scan" button

### Requirement: Serial Number Format Validation
The system SHALL validate the serial number input to ensure it follows the format PSN followed by exactly 9 digits (e.g., PSN123456789).

#### Scenario: Valid serial number format
- **WHEN** user enters "PSN123456789"
- **THEN** input is accepted and displayed in white color

#### Scenario: Invalid serial number - missing prefix
- **WHEN** user enters "123456789" (missing PSN prefix)
- **THEN** input is rejected and displayed in red color

#### Scenario: Invalid serial number - incorrect prefix
- **WHEN** user enters "SN123456789" (incorrect prefix)
- **THEN** input is rejected and displayed in red color

#### Scenario: Invalid serial number - wrong digit count
- **WHEN** user enters "PSN12345678" (only 8 digits)
- **THEN** input is rejected and displayed in red color

#### Scenario: Invalid serial number - contains non-digit characters
- **WHEN** user enters "PSN1234567A" (contains letter)
- **THEN** input is rejected and displayed in red color

#### Scenario: Empty input
- **WHEN** serial number input field is empty
- **THEN** no validation error is shown and field displays in default color

### Requirement: Serial Number Visual Feedback
The system SHALL provide visual feedback on the serial number input field based on validation state.

#### Scenario: Valid serial number display
- **WHEN** serial number format is valid
- **THEN** input field text color is white

#### Scenario: Invalid serial number display
- **WHEN** serial number format is invalid
- **THEN** input field text color is red

#### Scenario: Real-time validation
- **WHEN** user types in the serial number input field
- **THEN** validation is performed and visual feedback is updated immediately

### Requirement: Hide Unused Scan Buttons
The system SHALL hide the "Start Scan" and "Stop Scan" buttons in the "Scan Control" section as they are currently not used.

#### Scenario: Scan control button visibility
- **WHEN** application window is displayed
- **THEN** "Start Scan" and "Stop Scan" buttons are not visible

#### Scenario: Single Scan button remains visible
- **WHEN** application window is displayed
- **THEN** "Single Scan" button remains visible and functional

## ADDED Requirements

### Requirement: Device Connection
The system SHALL provide functionality to establish and terminate USB connections with the Siglent SDM4055A-SC multimeter using VISA protocol.

#### Scenario: Successful connection
- **WHEN** user clicks connect button and VISA device is available
- **THEN** connection is established and status indicator shows connected state

#### Scenario: Connection failure
- **WHEN** user clicks connect button and device is not available
- **THEN** error message is displayed and status indicator shows disconnected state

#### Scenario: Disconnection
- **WHEN** user clicks disconnect button while connected
- **THEN** connection is terminated gracefully and status indicator shows disconnected state

### Requirement: Multi-Channel Measurement Reading
The system SHALL read measurement data from multiple channels of the SDM4055A-SC multimeter with CS1016 scanning card at configurable intervals.

#### Scenario: Read DC voltage measurement
- **WHEN** device is connected and measurement function is set to DC voltage
- **THEN** system reads voltage value from device and returns it as float

#### Scenario: Periodic polling
- **WHEN** device is connected and polling timer is active
- **THEN** system reads measurement every 500ms and updates display

#### Scenario: Read during disconnection
- **WHEN** device is disconnected and polling timer attempts to read
- **THEN** system handles error gracefully and displays connection status

### Requirement: GUI Display
The system SHALL display measurement values on a modern digital indicator widget with card-style design and shadow effects.

#### Scenario: Display measurement value
- **WHEN** new measurement value is received from device
- **THEN** digital indicator widget updates to show the value with appropriate formatting

#### Scenario: Display connection status
- **WHEN** connection state changes
- **THEN** status indicator reflects current state (connected/disconnected/error)

#### Scenario: Apply dark theme
- **WHEN** application starts
- **THEN** qt-material dark_teal theme is applied globally to all widgets

### Requirement: Hardware Abstraction
The system SHALL provide a hardware abstraction layer that supports both real VISA device and simulator modes for development without physical hardware.

#### Scenario: Use real device
- **WHEN** application is configured to use real device mode
- **THEN** all communication is routed through VISA interface to actual SDM4055A-SC

#### Scenario: Use simulator
- **WHEN** application is configured to use simulator mode
- **THEN** all communication returns mock data without requiring physical device

#### Scenario: Switch between modes
- **WHEN** configuration changes between real device and simulator
- **THEN** system switches communication layer without requiring code changes

### Requirement: Error Handling
The system SHALL handle communication failures gracefully and provide user feedback.

#### Scenario: Timeout during read
- **WHEN** VISA read operation times out
- **THEN** system catches exception, logs error, and displays error message to user

#### Scenario: Device disconnection during polling
- **WHEN** device becomes disconnected while polling is active
- **THEN** system stops polling, updates status to disconnected, and displays error

#### Scenario: Invalid VISA resource
- **WHEN** specified VISA resource string is invalid or device not found
- **THEN** system displays clear error message indicating connection failure

### Requirement: Application Packaging
The system SHALL be packaged as a standalone Windows executable using PyInstaller with all dependencies included.

#### Scenario: Build executable
- **WHEN** build script is executed
- **THEN** PyInstaller creates standalone executable with qt-material hidden imports and data files

#### Scenario: Run executable
- **WHEN** user runs the packaged executable
- **THEN** application launches without requiring Python installation or additional dependencies

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
