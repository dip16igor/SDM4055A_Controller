# Change: Add Log Viewer Window

## Why
Users need visibility into application logs to diagnose issues, monitor system behavior, and understand what's happening during operation. Currently, logs are only visible in the console, which may not be easily accessible or visible during normal GUI usage. A dedicated log viewer window will provide real-time access to application logs with color-coded severity levels for better readability.

## What Changes
- Add a log viewer button in the status bar area (bottom left corner)
- Create a dockable/floating log viewer window that displays application logs
- Implement real-time log streaming from Python's logging system to the GUI
- Add color differentiation for different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Provide controls to clear logs, filter by log level, and auto-scroll
- Button should resemble a typical console/log icon and be positioned to the left of status text

## Impact
- Affected specs: `multimeter-controller`
- Affected code: 
  - `gui/window.py` - Add log viewer button and window
  - `gui/widgets.py` - Create LogViewerWidget component
  - `main.py` - Configure logging handler to emit signals to GUI
