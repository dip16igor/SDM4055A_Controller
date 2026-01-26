## ADDED Requirements

### Requirement: Theme Toggle Button
The system SHALL provide a theme toggle button in the status bar that allows users to switch between dark and light themes.

#### Scenario: Theme toggle button placement
- **WHEN** application window is displayed
- **THEN** theme toggle button is visible in the status bar
- **AND** button is positioned to the left of the log viewer button

#### Scenario: Theme toggle button appearance
- **WHEN** dark theme is active
- **THEN** button displays a sun icon
- **AND** button has tooltip "Switch to Light Theme"
- **WHEN** light theme is active
- **THEN** button displays a moon icon
- **AND** button has tooltip "Switch to Dark Theme"

#### Scenario: Toggle theme with button
- **WHEN** user clicks the theme toggle button
- **THEN** application theme switches to the opposite theme
- **AND** button icon updates to reflect the new theme
- **AND** tooltip updates to reflect the new theme option

#### Scenario: Theme toggle button size
- **WHEN** theme toggle button is displayed
- **THEN** button has fixed size of 30x30 pixels
- **AND** button styling matches log viewer button appearance

### Requirement: Theme Switching
The system SHALL support switching between dark and light themes using qt-material library themes.

#### Scenario: Switch from dark to light theme
- **WHEN** user clicks theme toggle button while dark theme is active
- **THEN** qt-material light_teal theme is applied to entire application
- **AND** all widgets update to light theme colors
- **AND** theme preference is saved for future sessions

#### Scenario: Switch from light to dark theme
- **WHEN** user clicks theme toggle button while light theme is active
- **THEN** qt-material dark_teal theme is applied to entire application
- **AND** all widgets update to dark theme colors
- **AND** theme preference is saved for future sessions

#### Scenario: Apply theme on startup
- **WHEN** application starts
- **THEN** saved theme preference is loaded and applied
- **AND** if no preference exists, dark theme is applied by default
- **AND** theme toggle button displays correct icon for current theme

### Requirement: Theme Persistence
The system SHALL persist user's theme preference across application sessions.

#### Scenario: Save theme preference
- **WHEN** user switches theme
- **THEN** current theme preference is saved using QSettings
- **AND** preference is stored with key "theme" and value "dark" or "light"

#### Scenario: Load theme preference
- **WHEN** application starts
- **THEN** theme preference is loaded from QSettings
- **AND** saved theme is applied to application
- **AND** if no preference exists, dark theme is applied by default

### Requirement: Log Viewer Theme Synchronization
The system SHALL ensure the log viewer window reflects the same theme as the main application.

#### Scenario: Log viewer theme on dark mode
- **WHEN** main application uses dark theme and log viewer is opened
- **THEN** log viewer dialog uses dark background (#2d2d2d)
- **AND** log text colors are optimized for dark background
- **AND** log viewer controls (buttons, dropdowns) use dark theme styling

#### Scenario: Log viewer theme on light mode
- **WHEN** main application uses light theme and log viewer is opened
- **THEN** log viewer dialog uses light background (#f5f5f5)
- **AND** log text colors are optimized for light background
- **AND** log viewer controls (buttons, dropdowns) use light theme styling

#### Scenario: Log viewer theme update on toggle
- **WHEN** user toggles theme while log viewer is open
- **THEN** log viewer dialog immediately updates to new theme
- **AND** all log viewer elements (background, text, controls) update styling
- **AND** existing log entries maintain readability with new colors

## MODIFIED Requirements

### Requirement: GUI Display
The system SHALL display measurement values on a modern digital indicator widget with card-style design and shadow effects, supporting both dark and light themes.

#### Scenario: Display measurement value
- **WHEN** new measurement value is received from device
- **THEN** digital indicator widget updates to show the value with appropriate formatting

#### Scenario: Display connection status
- **WHEN** connection state changes
- **THEN** status indicator reflects current state (connected/disconnected/error)

#### Scenario: Apply dark theme
- **WHEN** dark theme is active
- **THEN** qt-material dark_teal theme is applied globally to all widgets
- **AND** custom widget styles use dark background colors (#2d2d2d, #3d3d3d, etc.)
- **AND** text colors are white/light for readability

#### Scenario: Apply light theme
- **WHEN** light theme is active
- **THEN** qt-material light_teal theme is applied globally to all widgets
- **AND** custom widget styles use light background colors (#f5f5f5, #e0e0e0, etc.)
- **AND** text colors are dark for readability
