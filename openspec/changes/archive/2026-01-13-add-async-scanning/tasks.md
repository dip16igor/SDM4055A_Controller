## 1. Implementation

- [x] 1.1 Create async worker thread class for device operations
  - [x] 1.1.1 Create `hardware/async_worker.py` with QThread-based worker
  - [x] 1.1.2 Implement signals for measurement results, errors, and completion
  - [x] 1.1.3 Add support for cancellation and graceful shutdown
  - [x] 1.1.4 Implement periodic scan loop with configurable interval

- [x] 1.2 Refactor device interface for thread-safe operations
  - [x] 1.2.1 Review `hardware/visa_interface.py` for thread safety issues
  - [x] 1.2.2 Add thread-safe locking if needed for shared resources
  - [x] 1.2.3 Ensure connection/disconnection operations are thread-safe
  - [x] 1.2.4 Update `hardware/simulator.py` to match thread-safe interface

- [x] 1.3 Update MainWindow to use async worker
  - [x] 1.3.1 Replace QTimer-based scanning with QThread worker in `gui/window.py`
  - [x] 1.3.2 Connect worker signals to UI update methods
  - [x] 1.3.3 Implement proper worker lifecycle management (start, stop, cleanup)
  - [x] 1.3.4 Update START/STOP button handlers to control worker thread

- [x] 1.4 Add progress indicators to UI
  - [x] 1.4.1 Add visual scanning indicator (spinner or progress bar) to control panel
  - [x] 1.4.2 Implement channel highlighting during active reads
  - [x] 1.4.3 Add timestamp or scan counter to show scan activity
  - [x] 1.4.4 Ensure indicators update smoothly without flickering

- [x] 1.5 Implement error handling for async operations
  - [x] 1.5.1 Handle device timeouts in worker thread
  - [x] 1.5.2 Communicate errors to UI via signals
  - [x] 1.5.3 Display user-friendly error messages
  - [x] 1.5.4 Ensure errors don't crash the application

- [x] 1.6 Test UI responsiveness
  - [x] 1.6.1 Verify UI remains interactive during slow device operations
  - [x] 1.6.2 Test window operations (move, resize, minimize) while scanning
  - [x] 1.6.3 Verify all buttons and controls work during active scans
  - [x] 1.6.4 Test with simulator to verify async behavior

- [x] 1.7 Clean up and optimize
  - [x] 1.7.1 Remove old QTimer-based scanning code
  - [x] 1.7.2 Add logging for thread lifecycle events
  - [x] 1.7.3 Verify no memory leaks from thread creation/destruction
  - [x] 1.7.4 Add docstrings and comments for async patterns

## 2. Testing

- [x] 2.1 Unit tests for async worker
  - [x] 2.1.1 Test worker thread creation and lifecycle
  - [x] 2.1.2 Test signal emission and connection
  - [x] 2.1.3 Test cancellation and cleanup
  - [x] 2.1.4 Test error handling in worker thread

- [x] 2.2 Integration tests
  - [x] 2.2.1 Test full scan cycle with real device
  - [x] 2.2.2 Test with simulator
  - [x] 2.2.3 Test connection/disconnection during scanning
  - [x] 2.2.4 Test interval changes during active scanning

- [x] 2.3 UI responsiveness tests
  - [x] 2.3.1 Measure UI thread blocking time during scans
  - [x] 2.3.2 Test with intentionally slow device responses
  - [x] 2.3.3 Verify no UI freezing under various conditions
  - [x] 2.3.4 Test with multiple rapid user interactions

## 3. Documentation

- [x] 3.1 Update code documentation
  - [x] 3.1.1 Document async worker class and its signals
  - [x] 3.1.2 Add comments explaining thread safety considerations
  - [x] 3.1.3 Update MainWindow docstrings for async patterns

- [x] 3.2 Update user documentation
  - [x] 3.2.1 Document new progress indicators
  - [x] 3.2.2 Explain improved responsiveness
  - [x] 3.2.3 Note any changes in behavior from previous version
