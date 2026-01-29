## ADDED Requirements

### Requirement: Excel Export Button
The system SHALL provide a button labeled "xlsx" next to "New Report File" button for exporting CSV report to Excel format.

#### Scenario: Button placement
- **WHEN** user views the Scan Control section
- **THEN** "xlsx" button is positioned to the right of "New Report File" button
- **AND** button width is narrow to minimize UI space

#### Scenario: Button label
- **WHEN** user views the "xlsx" button
- **THEN** button displays short text "xlsx"

#### Scenario: Button enabled state
- **WHEN** no report file is selected
- **THEN** "xlsx" button is disabled
- **AND** user cannot click it

#### Scenario: Button enabled with report file
- **WHEN** a report file is selected
- **THEN** "xlsx" button is enabled
- **AND** user can click it to export to Excel

### Requirement: Excel Export with Conditional Formatting
The system SHALL export CSV report data to Excel (.xlsx) format with conditional formatting applied to measured value cells.

#### Scenario: Export with valid report file
- **WHEN** user clicks "xlsx" button and a valid CSV report file is selected
- **THEN** file save dialog opens with default filename matching report filename but with .xlsx extension
- **AND** user can choose save location
- **AND** Excel file is created with all data from CSV report
- **AND** conditional formatting is applied to measured value cells

#### Scenario: Export without report file
- **WHEN** user clicks "xlsx" button and no report file is selected
- **THEN** warning dialog is displayed indicating no report file is selected
- **AND** no export is performed

#### Scenario: Conditional formatting for values within thresholds
- **WHEN** a measured value is within configured lower and upper thresholds
- **THEN** cell background color is light green
- **AND** color is light enough for black text to be clearly readable

#### Scenario: Conditional formatting for values below lower threshold
- **WHEN** a measured value is below configured lower threshold
- **THEN** cell background color is light red
- **AND** color is light enough for black text to be clearly readable

#### Scenario: Conditional formatting for values above upper threshold
- **WHEN** a measured value is above configured upper threshold
- **THEN** cell background color is light red
- **AND** color is light enough for black text to be clearly readable

#### Scenario: Conditional formatting for values with only lower threshold
- **WHEN** a measured value is below configured lower threshold (no upper threshold set)
- **THEN** cell background color is light red

#### Scenario: Conditional formatting for values with only upper threshold
- **WHEN** a measured value is above configured upper threshold (no lower threshold set)
- **THEN** cell background color is light red

#### Scenario: Conditional formatting for values with no thresholds
- **WHEN** a measured value has no thresholds configured for its channel
- **THEN** cell has no conditional formatting applied
- **AND** cell uses default white background

#### Scenario: Conditional formatting for empty cells
- **WHEN** a cell contains no measurement data (empty string)
- **THEN** cell has no conditional formatting applied
- **AND** cell uses default white background

#### Scenario: Color contrast
- **WHEN** conditional formatting is applied to cells
- **THEN** background colors are light enough for black text to be clearly readable
- **AND** recommended colors are light red (#FFCCCC) and light green (#CCFFCC)

### Requirement: Excel File Format
The system SHALL create Excel files with the same structure as CSV reports but in .xlsx format.

#### Scenario: Header row preservation
- **WHEN** CSV report is exported to Excel
- **THEN** header row from CSV is preserved in Excel file
- **AND** column names match CSV exactly

#### Scenario: Data row preservation
- **WHEN** CSV report is exported to Excel
- **THEN** all data rows from CSV are preserved in Excel file
- **AND** cell values match CSV values exactly

#### Scenario: Date/Time column formatting
- **WHEN** CSV report is exported to Excel
- **THEN** Date/Time column values are preserved as text strings
- **AND** format matches CSV format (YYYY-MM-DD HH:MM:SS)

#### Scenario: Semicolon delimiter handling
- **WHEN** CSV report is exported to Excel
- **THEN** semicolon delimiters are converted to Excel cell boundaries
- **AND** each CSV field becomes a separate Excel cell

### Requirement: Export Error Handling
The system SHALL handle errors during Excel export gracefully with appropriate user feedback.

#### Scenario: Missing config file
- **WHEN** user clicks "xlsx" button but no config file is loaded
- **THEN** warning dialog is displayed indicating thresholds cannot be determined
- **AND** export proceeds without conditional formatting
- **AND** all values are exported with default formatting

#### Scenario: File write error
- **WHEN** Excel file cannot be written to selected location
- **THEN** error dialog is displayed with error details
- **AND** no file is created
- **AND** user can try again with different location

#### Scenario: Invalid CSV format
- **WHEN** CSV report file contains invalid or corrupted data
- **THEN** error dialog is displayed indicating parsing error
- **AND** export is aborted
- **AND** no Excel file is created

#### Scenario: Cancel export
- **WHEN** user cancels file save dialog
- **THEN** no export is performed
- **AND** no error is displayed
- **AND** UI remains unchanged
