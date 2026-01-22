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
 

### Requirement: Report File Selection
The system SHALL provide functionality to select an existing CSV report file for saving measurement results.

#### Scenario: Select existing report file
- **WHEN** user clicks "Select Report File" button
- **THEN** file dialog opens allowing user to select CSV files
- **AND** selected file path is stored for subsequent operations
- **AND** filename is displayed in UI with green color

#### Scenario: Report file not selected
- **WHEN** no report file has been selected
- **THEN** label displays "No report file selected" in gray italic text

### Requirement: New Report File Creation
The system SHALL provide functionality to create a new CSV report file with auto-generated filename.

#### Scenario: Create new report file with config loaded
- **WHEN** user clicks "New Report File" button and config file is loaded
- **THEN** file dialog opens with suggested filename: `<config_name>_<YYYY-MM-DD>.csv`
- **AND** user can save to any location
- **AND** empty CSV file is created
- **AND** filename is displayed in UI with green color

#### Scenario: Create new report file without config
- **WHEN** user clicks "New Report File" button and no config file is loaded
- **THEN** file dialog opens with suggested filename: `report_<YYYY-MM-DD>.csv`
- **AND** user can save to any location
- **AND** empty CSV file is created
- **AND** filename is displayed in UI with green color

#### Scenario: Cancel new report file creation
- **WHEN** user cancels file dialog
- **THEN** no file is created
- **AND** no changes are made to UI

### Requirement: Report File Format
The system SHALL write measurement results to CSV file with semicolon delimiter and specific column structure.

#### Scenario: Report file header with custom names
- **WHEN** report file is created or first row is written and channels have custom names configured
- **THEN** header row contains: "QR", "TEST RESULT", custom channel names for channels 1-12, "Date/Time"
- **AND** custom names are used instead of generic "Voltage1", "Voltage2", etc.

#### Scenario: Report file header without custom names
- **WHEN** report file is created or first row is written and no custom names are configured
- **THEN** header row contains: "QR", "TEST RESULT", "Voltage1" through "Voltage12", "Date/Time"

#### Scenario: Report file header with mixed custom names
- **WHEN** report file is created or first row is written and some channels have custom names while others do not
- **THEN** header row uses custom names for channels that have them
- **AND** uses generic names (e.g., "Voltage3") for channels without custom names

#### Scenario: Report data row format
- **WHEN** measurement results are written to report file
- **THEN** row contains:
  - Column 1: Serial number from Serial Number input field
  - Column 2: "OK" if all measurements within thresholds, "FAILED <details>" otherwise
  - Columns 3-14: Voltage measurements for channels 1-12 (empty for channels 13-16)
  - Column 15: Current timestamp in "YYYY-MM-DD HH:MM:SS" format

#### Scenario: Only voltage channels in report
- **WHEN** report row is written
- **THEN** only channels 1-12 (voltage channels) are included in report
- **AND** channels 13-16 (current channels) are not included

### Requirement: Serial Number Validation Before Scan
The system SHALL validate serial number format and presence before performing scan.

#### Scenario: Scan with missing serial number
- **WHEN** user clicks "Single Scan" with empty serial number field
- **THEN** warning dialog is displayed requesting user to enter serial number
- **AND** scan is not performed
- **AND** status shows "Scan complete - missing serial number"

#### Scenario: Scan with invalid serial number format
- **WHEN** user clicks "Single Scan" with invalid serial number format
- **THEN** warning dialog is displayed explaining required format (PSN + 9 digits)
- **AND** scan is not performed
- **AND** status shows "Scan complete - invalid serial number"

#### Scenario: Scan with valid serial number
- **WHEN** user clicks "Single Scan" with valid serial number (PSN + 9 digits)
- **THEN** scan is performed normally
- **AND** results are written to report file

### Requirement: Measurement Validation Against Thresholds
The system SHALL validate measurements against configured thresholds and generate appropriate result string.

#### Scenario: All measurements within thresholds
- **WHEN** all measured values are within configured thresholds
- **THEN** TEST RESULT column contains "OK"
- **AND** no failure details are included

#### Scenario: Measurement below lower threshold
- **WHEN** a measurement is below configured lower threshold
- **THEN** TEST RESULT column contains "FAILED" with details
- **AND** details include channel number, measured value, and expected range

#### Scenario: Measurement above upper threshold
- **WHEN** a measurement is above configured upper threshold
- **THEN** TEST RESULT column contains "FAILED" with details
- **AND** details include channel number, measured value, and expected range

#### Scenario: Multiple measurements outside thresholds
- **WHEN** multiple measurements are outside configured thresholds
- **THEN** TEST RESULT column contains "FAILED" with all failed channels separated by semicolons

#### Scenario: No thresholds configured
- **WHEN** no thresholds are configured for any channel
- **THEN** TEST RESULT column contains "OK" (no validation performed)

### Requirement: Report Row Update
The system SHALL update existing row if serial number already exists in report file, otherwise append new row.

#### Scenario: New serial number
- **WHEN** scan is performed with serial number not in report file
- **THEN** new row is appended to report file
- **AND** header row is added if file is empty

#### Scenario: Existing serial number
- **WHEN** scan is performed with serial number already in report file
- **THEN** existing row is updated with new measurements
- **AND** no duplicate rows are created

#### Scenario: Empty report file
- **WHEN** scan is performed on newly created report file
- **THEN** header row is added automatically
- **AND** data row is appended after header

### Requirement: Serial Number Color Coding
The system SHALL display serial number input field in different colors based on validation state and report file status.

#### Scenario: Invalid format
- **WHEN** serial number format is invalid
- **THEN** input field text color is red

#### Scenario: Valid format, not in report
- **WHEN** serial number format is valid but number is not in report file
- **THEN** input field text color is white

#### Scenario: Valid format, in report
- **WHEN** serial number format is valid and number exists in report file
- **THEN** input field text color is green with bold font weight

#### Scenario: Color update after scan
- **WHEN** scan is performed and data is written to report file
- **THEN** serial number input field color is updated to green
- **AND** user can see that number is now in report

### Requirement: Click-to-Clear Serial Number
The system SHALL clear serial number input field when user clicks on it, allowing easy entry of new serial number.

#### Scenario: Click on serial number field
- **WHEN** user clicks on serial number input field
- **THEN** existing text is cleared
- **AND** cursor appears in field for new input
- **AND** user can immediately type new serial number

#### Scenario: Prevent repeated clearing
- **WHEN** user clicks on serial number field multiple times without losing focus
- **THEN** field is cleared only on first click
- **AND** subsequent clicks do not clear text

#### Scenario: Reset clear flag on focus loss
- **WHEN** user clicks away from serial number field and then clicks back
- **THEN** field can be cleared again on new click

### Requirement: Report File Logging
The system SHALL provide detailed logging for all report file operations to facilitate debugging.

#### Scenario: Log report file selection
- **WHEN** user selects a report file
- **THEN** system logs file path and selection event

#### Scenario: Log report file creation
- **WHEN** user creates a new report file
- **THEN** system logs file path and creation event

#### Scenario: Log measurement validation
- **WHEN** measurements are validated against thresholds
- **THEN** system logs validation result and any failures

#### Scenario: Log report row write
- **WHEN** row is written to report file
- **THEN** system logs:
  - Serial number
  - Number of measurements
  - Validation result
  - Whether row was updated or appended
  - Total rows in file

#### Scenario: Log errors
- **WHEN** error occurs during report file operation
- **THEN** system logs error details and exception traceback
