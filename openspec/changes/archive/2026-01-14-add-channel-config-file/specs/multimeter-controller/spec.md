## ADDED Requirements

### Requirement: Configuration File Loading
The system SHALL support loading channel configurations from CSV files.

#### Scenario: Load valid configuration file
- **WHEN** user clicks "Load Config" button and selects a valid CSV file
- **THEN** system parses the configuration file
- **AND** applies measurement types to configured channels
- **AND** applies thresholds to configured channels
- **AND** displays configuration file name in UI
- **AND** shows success message with number of configured channels

#### Scenario: Load invalid configuration file
- **WHEN** user selects a CSV file with invalid format or data
- **THEN** system displays error message with specific validation failure
- **AND** does not apply any configuration
- **AND** keeps previous configuration unchanged

#### Scenario: Configuration file validation - channel numbers
- **WHEN** configuration file contains channel number outside 1-16 range
- **THEN** system rejects the file
- **AND** displays error message indicating invalid channel number

#### Scenario: Configuration file validation - measurement types
- **WHEN** configuration file contains invalid measurement type
- **THEN** system rejects the file
- **AND** displays error message listing valid measurement types

#### Scenario: Configuration file validation - channel type compatibility
- **WHEN** configuration file assigns current measurement to channels 1-12
- **THEN** system rejects the file
- **AND** displays error message indicating current not supported on those channels

#### Scenario: Configuration file validation - threshold consistency
- **WHEN** configuration file has lower threshold >= upper threshold
- **THEN** system rejects the file
- **AND** displays error message indicating thresholds must be valid

#### Scenario: Partial channel configuration
- **WHEN** configuration file contains only subset of channels (e.g., channels 1, 3, 5)
- **THEN** system applies configuration only to specified channels
- **AND** other channels remain unchanged

### Requirement: Threshold-Based Color Coding
The system SHALL display measurement values with color coding based on configured thresholds.

#### Scenario: Value within thresholds
- **WHEN** measured value is within configured lower and upper thresholds
- **THEN** value is displayed in GREEN color

#### Scenario: Value below lower threshold
- **WHEN** measured value is below configured lower threshold
- **THEN** value is displayed in RED color

#### Scenario: Value above upper threshold
- **WHEN** measured value is above configured upper threshold
- **THEN** value is displayed in RED color

#### Scenario: Threshold Display
- **WHEN** thresholds are configured for a channel
- **THEN** thresholds are displayed below the unit label
- **AND** lower threshold is shown as ">=value"
- **AND** upper threshold is shown as "<=value"
- **AND** both thresholds are separated by " | "
- **WHEN** no thresholds are configured
- **THEN** threshold display is hidden (empty string)

#### Scenario: Measurement Value Font Size
- **WHEN** viewing channel indicator
- **THEN** measurement value is displayed in 36pt font
- **AND** font is bold and monospace for readability

#### Scenario: No thresholds configured
- **WHEN** channel has no thresholds configured
- **THEN** value is displayed in default color (no threshold coloring)

#### Scenario: Only lower threshold configured
- **WHEN** channel has only lower threshold configured
- **THEN** values below threshold display in RED
- **AND** values at or above threshold display in GREEN

#### Scenario: Only upper threshold configured
- **WHEN** channel has only upper threshold configured
- **THEN** values above threshold display in RED
- **AND** values at or below threshold display in GREEN

### Requirement: Configuration File Format
The system SHALL support CSV format with specific columns.

#### Scenario: CSV file format
- **WHEN** creating configuration file
- **THEN** file must contain columns: channel, measurement_type, range, lower_threshold, upper_threshold
- **AND** channel column contains channel number (1-16)
- **AND** measurement_type column contains valid measurement type
- **AND** range column contains AUTO or specific range value
- **AND** lower_threshold column is optional (empty for no threshold)
- **AND** upper_threshold column is optional (empty for no threshold)

#### Scenario: Comment support
- **WHEN** CSV file contains lines starting with #
- **THEN** those lines are treated as comments and ignored during parsing

## MODIFIED Requirements

### Requirement: Channel Indicator Display
The channel indicator SHALL support threshold-based color coding.

#### Scenario: Apply thresholds to channel
- **WHEN** configuration is loaded with thresholds for a channel
- **THEN** channel indicator stores threshold values
- **AND** applies color coding to displayed values

#### Scenario: Clear thresholds from channel
- **WHEN** new configuration is loaded without thresholds for a previously configured channel
- **THEN** channel indicator clears threshold values
- **AND** displays values in default color

### Requirement: Scan Control UI
The scan control section SHALL include configuration file loading controls.

#### Scenario: Load Config button placement
- **WHEN** viewing Scan Control section
- **THEN** "Load Config" button is displayed to the right of scan buttons
- **AND** configuration file name label is displayed next to button

#### Scenario: Configuration file name display
- **WHEN** configuration file is loaded
- **THEN** file name is displayed in green color
- **WHEN** no configuration is loaded
- **THEN** "No config loaded" is displayed in gray italic text
