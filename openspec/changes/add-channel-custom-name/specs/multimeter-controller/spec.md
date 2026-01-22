## ADDED Requirements

### Requirement: Channel Custom Name Field
The system SHALL support an optional custom name field for each channel in the configuration CSV file.

#### Scenario: Load configuration with custom names
- **WHEN** configuration file contains custom names for channels
- **THEN** custom names are loaded and stored for each channel
- **AND** custom names are available for use in report generation

#### Scenario: Load configuration without custom names
- **WHEN** configuration file does not contain custom name column or has empty values
- **THEN** system loads configuration successfully without custom names
- **AND** channels are identified by their numeric IDs only

#### Scenario: Configuration file with Name field
- **WHEN** configuration file has the format: channel,Name,measurement_type,range,lower_threshold,upper_threshold
- **THEN** Name field is parsed as the second column
- **AND** Name field value is stripped of leading/trailing whitespace
- **AND** empty Name values are allowed and treated as no custom name

#### Scenario: Backward compatibility
- **WHEN** old configuration file format is loaded (without Name column)
- **THEN** system loads configuration successfully
- **AND** all channels function normally without custom names

### Requirement: CSV Whitespace Handling
The system SHALL correctly parse CSV files with whitespace in field values.

#### Scenario: Whitespace in field values
- **WHEN** configuration file contains spaces around field values (e.g., " 1 , Testing , VOLT:DC , 200 mV ,150 , 180 ")
- **THEN** fields are parsed correctly after stripping whitespace
- **AND** configuration loads successfully

#### Scenario: Whitespace in custom names
- **WHEN** custom name contains internal spaces (e.g., "Test Point 3")
- **THEN** internal spaces are preserved
- **AND** only leading/trailing whitespace is stripped

### Requirement: Custom Name in Report Headers
The system SHALL use custom channel names in report file headers when available.

#### Scenario: Report with custom names
- **WHEN** channels have custom names configured
- **THEN** report file header uses custom names instead of generic "Voltage1", "Voltage2", etc.
- **AND** header format becomes: "QR", "TEST RESULT", "<CustomName1>", "<CustomName2>", ..., "Date/Time"

#### Scenario: Report with mixed custom names
- **WHEN** some channels have custom names and others do not
- **THEN** report header uses custom names for channels that have them
- **AND** uses generic names (e.g., "Voltage3") for channels without custom names

#### Scenario: Report without custom names
- **WHEN** no channels have custom names configured
- **THEN** report header uses generic names (e.g., "Voltage1", "Voltage2", etc.)

### Requirement: Channel Name Storage
The system SHALL store custom channel names in the ChannelThresholdConfig data structure.

#### Scenario: Store custom name
- **WHEN** channel configuration is loaded with a custom name
- **THEN** custom name is stored in the ChannelThresholdConfig object
- **AND** custom name can be retrieved via getter method

#### Scenario: Retrieve custom name
- **WHEN** custom name is requested for a channel
- **THEN** custom name is returned if configured
- **AND** empty string or None is returned if no custom name is configured
