## ADDED Requirements

### Requirement: Single Scan
The system SHALL provide a single scan button that performs a one-time measurement of all channels without starting continuous polling.

#### Scenario: Successful single scan
- **WHEN** user clicks single scan button while device is connected
- **THEN** system reads all channels once and updates display with measured values
- **AND** scan status indicates "Scan complete"

#### Scenario: Single scan while continuous scanning is active
- **WHEN** user clicks single scan button while continuous scanning is running
- **THEN** single scan is performed independently
- **AND** continuous scanning continues uninterrupted

#### Scenario: Single scan while disconnected
- **WHEN** user clicks single scan button while device is disconnected
- **THEN** system displays warning message
- **AND** no scan is performed

#### Scenario: Single scan button state
- **WHEN** device is connected
- **THEN** single scan button is enabled
- **WHEN** device is disconnected
- **THEN** single scan button is disabled
