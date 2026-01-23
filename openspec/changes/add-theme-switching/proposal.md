# Change: Add Theme Switching Button

## Why
The application currently only supports a dark theme, which may not be suitable for all users or lighting conditions. Users need the ability to switch between dark and light themes to improve usability and readability in different environments. Additionally, the log viewer window should reflect the same theme as the main application for consistency.

## What Changes
- Add a theme toggle button in the status bar, positioned to the left of the log viewer button
- Implement light theme support using qt-material library (light_teal theme)
- Add theme state management to persist user's theme preference
- Ensure log viewer window dynamically updates its styling when theme is toggled
- Apply appropriate styling to the theme toggle button for both dark and light themes

## Impact
- Affected specs: multimeter-controller
- Affected code: 
  - `main.py` - theme application logic
  - `gui/window.py` - theme toggle button and theme management
  - `gui/widgets.py` - log viewer dialog theme support
