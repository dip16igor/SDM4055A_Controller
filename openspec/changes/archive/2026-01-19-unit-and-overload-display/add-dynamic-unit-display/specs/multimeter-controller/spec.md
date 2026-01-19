## ADDED Requirements

### Requirement: Dynamic Unit Display
The system SHALL automatically update the unit label displayed on each channel indicator based on the selected measurement type.

#### Scenario: Unit updates to V when voltage measurement selected
- **WHEN** user selects "DC Voltage" or "AC Voltage" measurement type for a channel
- **THEN** the unit label for that channel displays "V"

#### Scenario: Unit updates to A when current measurement selected
- **WHEN** user selects "DC Current" or "AC Current" measurement type for a channel
- **THEN** the unit label for that channel displays "A"

#### Scenario: Unit updates to Ohm when resistance measurement selected
- **WHEN** user selects "2-Wire Resistance" or "4-Wire Resistance" measurement type for a channel
- **THEN** the unit label for that channel displays "Ohm"

#### Scenario: Unit updates to F when capacitance measurement selected
- **WHEN** user selects "Capacitance" measurement type for a channel
- **THEN** the unit label for that channel displays "F"

#### Scenario: Unit updates to Hz when frequency measurement selected
- **WHEN** user selects "Frequency" measurement type for a channel
- **THEN** the unit label for that channel displays "Hz"

#### Scenario: Unit updates to V when diode measurement selected
- **WHEN** user selects "Diode" measurement type for a channel
- **THEN** the unit label for that channel displays "V"

#### Scenario: Unit updates to Ohm when continuity measurement selected
- **WHEN** user selects "Continuity" measurement type for a channel
- **THEN** the unit label for that channel displays "Ohm"

#### Scenario: Unit updates to C when temperature measurement selected
- **WHEN** user selects "RTD Temperature" or "Thermocouple" measurement type for a channel
- **THEN** the unit label for that channel displays "C"

#### Scenario: Unit updates when measurement type changed manually
- **WHEN** user changes measurement type selection from dropdown for a channel
- **THEN** unit label immediately updates to reflect the new measurement type

#### Scenario: Unit updates when configuration file loaded
- **WHEN** user loads a configuration file with measurement types for channels
- **THEN** unit labels for all configured channels update to reflect their respective measurement types

#### Scenario: Unit persists across scans
- **WHEN** measurement type is set and multiple scans are performed
- **THEN** unit label remains consistent with the selected measurement type across all scans
