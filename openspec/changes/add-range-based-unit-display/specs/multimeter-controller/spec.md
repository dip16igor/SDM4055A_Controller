## ADDED Requirements

### Requirement: Range-Based Unit Display
The system SHALL automatically update the unit label displayed on each channel indicator based on both the selected measurement type and the selected measurement range.

#### Scenario: Unit displays mV when 200 mV range selected for voltage
- **WHEN** user selects "200 mV" range for voltage measurement
- **THEN** the unit label for that channel displays "mV"

#### Scenario: Unit displays V when 2 V range selected for voltage
- **WHEN** user selects "2 V" range for voltage measurement
- **THEN** the unit label for that channel displays "V"

#### Scenario: Unit displays uA when 200 uA range selected for current
- **WHEN** user selects "200 uA" range for current measurement
- **THEN** the unit label for that channel displays "uA"

#### Scenario: Unit displays mA when 2 mA range selected for current
- **WHEN** user selects "2 mA" range for current measurement
- **THEN** the unit label for that channel displays "mA"

#### Scenario: Unit displays A when 2 A range selected for current
- **WHEN** user selects "2 A" range for current measurement
- **THEN** the unit label for that channel displays "A"

#### Scenario: Unit displays nF when 2 nF range selected for capacitance
- **WHEN** user selects "2 nF" range for capacitance measurement
- **THEN** the unit label for that channel displays "nF"

#### Scenario: Unit displays uF when 2 uF range selected for capacitance
- **WHEN** user selects "2 uF" range for capacitance measurement
- **THEN** the unit label for that channel displays "uF"

#### Scenario: Unit displays Ohm when 200 Ohm range selected for resistance
- **WHEN** user selects "200 Ohm" range for resistance measurement
- **THEN** the unit label for that channel displays "Ohm"

#### Scenario: Unit displays kOhm when 2 kOhm range selected for resistance
- **WHEN** user selects "2 kOhm" range for resistance measurement
- **THEN** the unit label for that channel displays "kOhm"

#### Scenario: Unit updates when range is changed manually
- **WHEN** user changes range selection from dropdown for a channel
- **THEN** unit label immediately updates to reflect the new range-based unit

#### Scenario: Unit updates when configuration file with ranges is loaded
- **WHEN** user loads a configuration file with range values for channels
- **THEN** unit labels for all configured channels update to reflect their respective range-based units

#### Scenario: Range dropdown shows appropriate options for measurement type
- **WHEN** user selects a measurement type for a channel
- **THEN** the range dropdown displays only valid ranges for that measurement type
