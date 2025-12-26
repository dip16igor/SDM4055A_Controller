## ADDED Requirements

### Requirement: Multi-Channel Support
The system SHALL support scanning and displaying measurements from up to 16 channels using the CS1016 scanning card connected to the SDM4055A-SC multimeter.

#### Scenario: Initialize 16 channels
- **WHEN** application starts with CS1016 card connected
- **THEN** system initializes all 16 channels and prepares them for scanning

#### Scenario: Scan all channels
- **WHEN** scanning is active
- **THEN** system sequentially reads measurements from all 16 channels and updates their displays

### Requirement: Channel Measurement Types
The system SHALL support different measurement types per channel based on channel number and hardware capabilities.

#### Scenario: Configure voltage measurement
- **WHEN** user selects DC or AC voltage for a channel (1-12)
- **THEN** system configures that channel for voltage measurement and displays voltage unit (V)

#### Scenario: Configure resistance measurement
- **WHEN** user selects 2-wire or 4-wire resistance for a channel (1-12)
- **THEN** system configures that channel for resistance measurement and displays ohm unit (Ω)

#### Scenario: Configure capacitance measurement
- **WHEN** user selects capacitance for a channel (1-12)
- **THEN** system configures that channel for capacitance measurement and displays farad unit (F)

#### Scenario: Configure frequency measurement
- **WHEN** user selects frequency for a channel (1-12)
- **THEN** system configures that channel for frequency measurement and displays hertz unit (Hz)

#### Scenario: Configure diode/continuity measurement
- **WHEN** user selects diode or continuity for a channel (1-12)
- **THEN** system configures that channel for diode test and displays appropriate indicator

#### Scenario: Configure temperature measurement
- **WHEN** user selects RTD or thermocouple for a channel (1-12)
- **THEN** system configures that channel for temperature measurement and displays degree unit (°C or °F)

#### Scenario: Configure current measurement
- **WHEN** user selects AC or DC current for a channel (13-16)
- **THEN** system configures that channel for current measurement and displays ampere unit (A)

### Requirement: Channel Display
The system SHALL display all 16 channels with modern digital indicators showing measurement values and appropriate unit labels.

#### Scenario: Display channel measurements
- **WHEN** scanning is active and measurements are available
- **THEN** each channel indicator shows current value with proper formatting and unit label

#### Scenario: Large readable indicators
- **WHEN** application displays channels
- **THEN** indicator widgets are sized appropriately for easy reading from typical viewing distance

#### Scenario: Channel numbering
- **WHEN** channels are displayed
- **THEN** each channel is clearly numbered (1-16) for identification

### Requirement: Scanning Controls
The system SHALL provide START and STOP buttons to control the scanning process.

#### Scenario: Start scanning
- **WHEN** user clicks START button and device is connected
- **THEN** scanning begins and measurements are read at configured interval

#### Scenario: Stop scanning
- **WHEN** user clicks STOP button while scanning is active
- **THEN** scanning stops immediately and no further measurements are read

#### Scenario: Start without connection
- **WHEN** user clicks START button and device is not connected
- **THEN** system displays error message and does not start scanning

#### Scenario: Button state management
- **WHEN** scanning state changes
- **THEN** START/STOP buttons reflect current state (disabled/enabled appropriately)

### Requirement: Scan Interval Configuration
The system SHALL allow users to configure the scanning interval from 100ms to 5 seconds using a slider control.

#### Scenario: Adjust scan interval
- **WHEN** user moves the scan interval slider
- **THEN** scanning interval updates immediately and is displayed to user

#### Scenario: Default interval
- **WHEN** application starts
- **THEN** scan interval is set to 1 second (1000ms) by default

#### Scenario: Minimum interval
- **WHEN** user sets slider to minimum position
- **THEN** scan interval is set to 100ms

#### Scenario: Maximum interval
- **WHEN** user sets slider to maximum position
- **THEN** scan interval is set to 5000ms (5 seconds)

### Requirement: Device Address Display
The system SHALL display the USB device address at the top of the interface.

#### Scenario: Display connected device address
- **WHEN** device is successfully connected
- **THEN** USB device address is displayed at top of interface

#### Scenario: No device connected
- **WHEN** no device is connected
- **THEN** device address field shows "Not connected" or similar status

#### Scenario: Update address on reconnection
- **WHEN** user disconnects and reconnects to device
- **THEN** device address display updates to show new connection address

### Requirement: Channel Configuration UI
The system SHALL provide user interface elements for configuring measurement types per channel.

#### Scenario: Voltage/resistance/capacitance/frequency/diode/temperature selection
- **WHEN** user interacts with channel configuration for channels 1-12
- **THEN** dropdown or selection control shows available measurement types (DC voltage, AC voltage, 2-wire resistance, 4-wire resistance, capacitance, frequency, diode, continuity, RTD temperature, thermocouple temperature)

#### Scenario: Current measurement selection
- **WHEN** user interacts with channel configuration for channels 13-16
- **THEN** dropdown or selection control shows AC current and DC current options

#### Scenario: Persist configuration
- **WHEN** user changes measurement type for a channel
- **THEN** configuration is applied immediately and subsequent scans use new measurement type
