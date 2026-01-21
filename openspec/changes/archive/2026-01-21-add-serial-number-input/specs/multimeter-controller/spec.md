## ADDED Requirements

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
