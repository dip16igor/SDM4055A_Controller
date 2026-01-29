# Change: Add Excel Export with Conditional Formatting

## Why
Users need to export CSV measurement reports to Excel format with visual highlighting of values that are outside configured thresholds. This makes it easier to quickly identify failed measurements in a spreadsheet format that supports filtering, sorting, and additional analysis.

## What Changes
- Add a small "xlsx" button next to "New Report File" button in the Scan Control section
- Button width should be narrow to minimize UI space
- When clicked, export the currently open CSV report file to Excel (.xlsx) format
- Apply conditional formatting to measured value cells:
  - Light red background for values outside thresholds (below lower or above upper)
  - Light green background for values within thresholds
  - Colors must be light enough for black text to be clearly readable
- Open standard save file dialog with default filename matching the report filename but with .xlsx extension
- Read threshold configuration from loaded config file to determine which values are in/out of range

## Impact
- Affected specs: multimeter-controller
- Affected code: gui/window.py (add button and export logic)
- New dependency: openpyxl library for Excel file creation and conditional formatting
