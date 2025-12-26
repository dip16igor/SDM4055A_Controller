# Multimeter Controller

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
