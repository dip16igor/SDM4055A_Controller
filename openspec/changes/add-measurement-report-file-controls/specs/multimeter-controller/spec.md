## ADDED Requirements

### Requirement: Report File Selection Button
The system SHALL provide a "Select Report File" button in the "Scan Control" section to allow users to choose an existing CSV file for saving measurement data.

#### Scenario: Display select report file button
- **WHEN** application window is displayed
- **THEN** "Select Report File" button is visible in the "Scan Control" section

#### Scenario: Open file dialog on button click
- **WHEN** user clicks "Select Report File" button
- **THEN** file dialog opens with CSV filter and allows user to select an existing CSV file

#### Scenario: Store selected file path
- **WHEN** user selects a CSV file from the dialog
- **THEN** selected file path is stored in application state and filename is displayed

### Requirement: New Report File Button
The system SHALL provide a "New Report File" button in the "Scan Control" section to allow users to create a new CSV file with an auto-generated name.

#### Scenario: Display new report file button
- **WHEN** application window is displayed
- **THEN** "New Report File" button is visible in the "Scan Control" section

#### Scenario: Create file with auto-generated name
- **WHEN** user clicks "New Report File" button
- **THEN** a new CSV file is created with auto-generated name and file path is stored

### Requirement: Auto-Generated Report Filename
The system SHALL generate report filenames using the configuration file name (without extension) and the current date in YYYY-MM-DD format.

#### Scenario: Generate filename with config file name
- **WHEN** a configuration file named "test_config.csv" is loaded and user creates a new report file
- **THEN** report filename is "test_config_2026-01-21.csv" (or current date)

#### Scenario: Generate filename without config file
- **WHEN** no configuration file is loaded and user creates a new report file
- **THEN** report filename is "report_2026-01-21.csv" (or current date)

#### Scenario: Generate filename with date format
- **WHEN** generating a report filename
- **THEN** date portion follows YYYY-MM-DD format (e.g., 2026-01-21)

### Requirement: Report Filename Display
The system SHALL display the current report filename next to the file selection buttons in the "Scan Control" section.

#### Scenario: Display filename after selection
- **WHEN** user selects a report file
- **THEN** selected filename is displayed next to the buttons

#### Scenario: Display filename after creation
- **WHEN** user creates a new report file
- **THEN** created filename is displayed next to the buttons

#### Scenario: Display empty state
- **WHEN** no report file has been selected or created
- **THEN** filename display shows "No report file selected" or similar placeholder text

### Requirement: Report File Storage
The system SHALL store the selected report file path in the application state for later use when writing measurement data.

#### Scenario: Store file path after selection
- **WHEN** user selects a report file
- **THEN** file path is stored in application instance variable

#### Scenario: Store file path after creation
- **WHEN** user creates a new report file
- **THEN** file path is stored in application instance variable

#### Scenario: Update stored path on new selection
- **WHEN** user selects a different report file
- **THEN** stored file path is updated to the new selection
