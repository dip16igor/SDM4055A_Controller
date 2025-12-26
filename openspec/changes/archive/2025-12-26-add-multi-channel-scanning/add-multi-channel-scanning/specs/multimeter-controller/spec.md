## MODIFIED Requirements

### Requirement: Multi-Channel Measurement Reading
The system SHALL read measurement data from multiple channels of the SDM4055A-SC multimeter with CS1016 scanning card at configurable intervals.

#### Scenario: Read single channel measurement
- **WHEN** device is connected and specific channel is selected
- **THEN** system reads measurement value from specified channel and returns it as float

#### Scenario: Read all channels in sequence
- **WHEN** device is connected and multi-channel scanning is active
- **THEN** system cycles through all 16 channels, reading each measurement sequentially

#### Scenario: Periodic multi-channel polling
- **WHEN** device is connected and polling timer is active
- **THEN** system reads measurements from all channels at configured interval (100ms-5s, default 1s) and updates all displays

#### Scenario: Read during disconnection
- **WHEN** device is disconnected and polling timer attempts to read
- **THEN** system handles error gracefully and displays connection status for all channels

### Requirement: Device Connection
The system SHALL provide functionality to establish and terminate USB connections with the Siglent SDM4055A-SC multimeter using VISA protocol, with support for CS1016 scanning card detection.

#### Scenario: Successful connection with CS1016 card
- **WHEN** user clicks connect button and VISA device with CS1016 card is available
- **THEN** connection is established, CS1016 card is detected, and status indicator shows connected state with device address

#### Scenario: Connection failure
- **WHEN** user clicks connect button and device is not available
- **THEN** error message is displayed and status indicator shows disconnected state

#### Scenario: Disconnection
- **WHEN** user clicks disconnect button while connected
- **THEN** connection is terminated gracefully, all channels are reset, and status indicator shows disconnected state

#### Scenario: Display device address
- **WHEN** device is successfully connected
- **THEN** USB device address is displayed at the top of the interface
