## 1. Implementation
- [ ] 1.1 Create LogViewerWidget class in gui/widgets.py
  - [ ] 1.1.1 Implement QTextEdit-based log display widget
  - [ ] 1.1.2 Add color formatting for different log levels (DEBUG: gray, INFO: white, WARNING: yellow, ERROR: red, CRITICAL: magenta)
  - [ ] 1.1.3 Implement auto-scroll to latest log entry
  - [ ] 1.1.4 Add clear logs button
  - [ ] 1.1.5 Add log level filter dropdown (All, DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - [ ] 1.1.6 Add method to append log entries with timestamp and color

- [ ] 1.2 Create QLogHandler class in gui/window.py or gui/widgets.py
  - [ ] 1.2.1 Extend logging.Handler to emit Qt signals
  - [ ] 1.2.2 Implement emit() method to send log records to GUI
  - [ ] 1.2.3 Format log messages with timestamp, level, and message

- [ ] 1.3 Add log viewer button to MainWindow in gui/window.py
  - [ ] 1.3.1 Create QPushButton with console/log icon (use built-in Qt icon or Unicode character)
  - [ ] 1.3.2 Position button in status bar (bottom left corner)
  - [ ] 1.3.3 Place button to the left of status text
  - [ ] 1.3.4 Set button tooltip to "Open Log Viewer"

- [ ] 1.4 Create log viewer window/dialog in gui/window.py
  - [ ] 1.4.1 Create QDialog or QMainWindow for log viewer
  - [ ] 1.4.2 Add LogViewerWidget as central widget
  - [ ] 1.4.3 Add toolbar with clear and filter controls
  - [ ] 1.4.4 Set window title "Application Logs"
  - [ ] 1.4.5 Set initial size (e.g., 800x600)
  - [ ] 1.4.6 Make window dockable or floating (optional)

- [ ] 1.5 Connect log viewer button to window toggle in gui/window.py
  - [ ] 1.5.1 Create slot to show/hide log viewer window
  - [ ] 1.5.2 Connect button clicked signal to toggle slot
  - [ ] 1.5.3 Update button state to reflect window visibility

- [ ] 1.6 Configure logging in main.py
  - [ ] 1.6.1 Add QLogHandler to root logger
  - [ ] 1.6.2 Connect QLogHandler signals to LogViewerWidget
  - [ ] 1.6.3 Ensure existing logging configuration is preserved
  - [ ] 1.6.4 Test that all log messages appear in viewer

- [ ] 1.7 Style the log viewer window
  - [ ] 1.7.1 Apply dark theme consistent with rest of application
  - [ ] 1.7.2 Set appropriate font for log display (monospace preferred)
  - [ ] 1.7.3 Ensure good contrast for colored log levels
  - [ ] 1.7.4 Style buttons and controls to match application theme

- [ ] 1.8 Test log viewer functionality
  - [ ] 1.8.1 Verify button appears in correct position (bottom left, left of status text)
  - [ ] 1.8.2 Verify log viewer window opens on button click
  - [ ] 1.8.3 Verify logs appear in real-time as they are generated
  - [ ] 1.8.4 Verify color differentiation works for all log levels
  - [ ] 1.8.5 Verify clear logs button works
  - [ ] 1.8.6 Verify log level filter works
  - [ ] 1.8.7 Verify auto-scroll to latest entry works
  - [ ] 1.8.8 Verify window can be closed and reopened
  - [ ] 1.8.9 Verify logs persist across window close/reopen
