## MODIFIED Requirements

### Requirement: Channel Indicator Value Display
The channel indicator SHALL display measurement values with inline units.

#### Scenario: Inline unit display
- **WHEN** viewing a channel indicator
- **THEN** measurement value and unit are displayed on the same line
- **AND** format is "{value} {unit}" (e.g., "5.001619 V")
- **AND** unit is separated from value by a single space

#### Scenario: Measurement value font size
- **WHEN** viewing a channel indicator
- **THEN** measurement value (including unit) is displayed in 42pt font
- **AND** font is bold and monospace for readability
- **AND** font family is "Consolas, Courier New, monospace"

#### Scenario: Value display with various units
- **WHEN** displaying measurement with unit "V"
- **THEN** display shows value followed by " V" (e.g., "5.001619 V")
- **WHEN** displaying measurement with unit "mV"
- **THEN** display shows value followed by " mV" (e.g., "123.456789 mV")
- **WHEN** displaying measurement with unit "A"
- **THEN** display shows value followed by " A" (e.g., "1.234567 A")
- **WHEN** displaying measurement with unit "Ohm"
- **THEN** display shows value followed by " Ohm" (e.g., "1000.000000 Ohm")
- **WHEN** displaying measurement with unit "kOhm"
- **THEN** display shows value followed by " kOhm" (e.g., "1.000000 kOhm")
- **WHEN** displaying measurement with unit "MOhm"
- **THEN** display shows value followed by " MOhm" (e.g., "1.000000 MOhm")
- **WHEN** displaying measurement with unit "uF"
- **THEN** display shows value followed by " uF" (e.g., "10.000000 uF")
- **WHEN** displaying measurement with unit "nF"
- **THEN** display shows value followed by " nF" (e.g., "100.000000 nF")
- **WHEN** displaying measurement with unit "Hz"
- **THEN** display shows value followed by " Hz" (e.g., "60.000000 Hz")
- **WHEN** displaying measurement with unit "C"
- **THEN** display shows value followed by " C" (e.g., "25.000000 C")

#### Scenario: Value display with status messages
- **WHEN** channel is disconnected
- **THEN** value label displays "Disconnected"
- **AND** no unit is displayed
- **WHEN** channel has error
- **THEN** value label displays error message
- **AND** no unit is displayed
- **AND** text is displayed in red color

#### Scenario: Dynamic unit updates
- **WHEN** user changes measurement type
- **THEN** unit in value display updates immediately
- **AND** value is refreshed with new unit
- **WHEN** user changes range
- **THEN** unit in value display updates immediately if range-specific unit differs
- **AND** value is refreshed with new unit

#### Scenario: Threshold color coding with inline units
- **WHEN** thresholds are configured and value is within thresholds
- **THEN** entire value text (including unit) is displayed in GREEN color
- **WHEN** thresholds are configured and value is outside thresholds
- **THEN** entire value text (including unit) is displayed in RED color
- **WHEN** no thresholds are configured
- **THEN** value text is displayed in default color

#### Scenario: Compact layout
- **WHEN** viewing multiple channel indicators
- **THEN** vertical space usage is reduced compared to previous layout
- **AND** more channels fit on screen at once
- **AND** layout remains readable with 42pt font

### Requirement: Channel Indicator Layout
The channel indicator layout SHALL accommodate inline unit display.

#### Scenario: Removed unit label
- **WHEN** viewing channel indicator layout
- **THEN** separate unit label widget is not present
- **AND** unit is part of value label text

#### Scenario: Adjusted vertical spacing
- **WHEN** viewing channel indicator layout
- **THEN** vertical spacing between elements is optimized for larger font
- **AND** layout remains balanced and readable

#### Scenario: Layout consistency
- **WHEN** comparing multiple channel indicators
- **THEN** all indicators have consistent layout
- **AND** all use inline unit display
- **AND** all use 42pt font for values
