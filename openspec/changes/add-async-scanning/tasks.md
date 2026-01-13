## 1. Implementation

- [ ] 1.1 Create async worker thread class for device operations
  - [ ] 1.1.1 Create `hardware/async_worker.py` with QThread-based worker
  - [ ] 1.1.2 Implement signals for measurement results, errors, and completion
  - [ ] 1.1.3 Add support for cancellation and graceful shutdown
  - [ ] 1.1.4 Implement periodic scan loop with configurable interval

- [ ] 1.2 Refactor device interface for thread-safe operations
  - [ ] 1.2.1 Review `hardware/visa_interface.py` for thread safety issues
  - [ ] 1.2.2 Add thread-safe locking if needed for shared resources
  - [ ] 1.2.3 Ensure connection/disconnection operations are thread-safe
  - [ ] 1.2.4 Update `hardware/simulator.py` to match thread-safe interface

- [ ] 1.3 Update MainWindow to use async worker
  - [ ] 1.3.1 Replace QTimer-based scanning with QThread worker in `gui/window.py`
  - [ ] 1.3.2 Connect worker signals to UI update methods
  - [ ] 1.3.3 Implement proper worker lifecycle management (start, stop, cleanup)
  - [ ] 1.3.4 Update START/STOP button handlers to control worker thread

- [ ] 1.4 Add progress indicators to UI
  - [ ] 1.4.1 Add visual scanning indicator (spinner or progress bar) to control panel
  - [ ] 1.4.2 Implement channel highlighting during active reads
  - [ ] 1.4.3 Add timestamp or scan counter to show scan activity
  - [ ] 1.4.4 Ensure indicators update smoothly without flickering

- [ ] 1.5 Implement error handling for async operations
  - [ ] 1.5.1 Handle device timeouts in worker thread
  - [ ] 1.5.2 Communicate errors to UI via signals
  - [ ] 1.5.3 Display user-friendly error messages
  - [ ] 1.5.4 Ensure errors don't crash the application

- [ ] 1.6 Test UI responsiveness
  - [ ] 1.6.1 Verify UI remains interactive during slow device operations
  - [ ] 1.6.2 Test window operations (move, resize, minimize) while scanning
  - [ ] 1.6.3 Verify all buttons and controls work during active scans
  - [ ] 1.6.4 Test with simulator to verify async behavior

- [ ] 1.7 Clean up and optimize
  - [ ] 1.7.1 Remove old QTimer-based scanning code
  - [ ] 1.7.2 Add logging for thread lifecycle events
  - [ ] 1.7.3 Verify no memory leaks from thread creation/destruction
  - [ ] 1.7.4 Add docstrings and comments for async patterns

## 2. Testing

- [ ] 2.1 Unit tests for async worker
  - [ ] 2.1.1 Test worker thread creation and lifecycle
  - [ ] 2.1.2 Test signal emission and connection
  - [ ] 2.1.3 Test cancellation and cleanup
  - [ ] 2.1.4 Test error handling in worker thread

- [ ] 2.2 Integration tests
  - [ ] 2.2.1 Test full scan cycle with real device
  - [ ] 2.2.2 Test with simulator
  - [ ] 2.2.3 Test connection/disconnection during scanning
  - [ ] 2.2.4 Test interval changes during active scanning

- [ ] 2.3 UI responsiveness tests
  - [ ] 2.3.1 Measure UI thread blocking time during scans
  - [ ] 2.3.2 Test with intentionally slow device responses
  - [ ] 2.3.3 Verify no UI freezing under various conditions
  - [ ] 2.3.4 Test with multiple rapid user interactions

## 3. Documentation

- [ ] 3.1 Update code documentation
  - [ ] 3.1.1 Document async worker class and its signals
  - [ ] 3.1.2 Add comments explaining thread safety considerations
  - [ ] 3.1.3 Update MainWindow docstrings for async patterns

- [ ] 3.2 Update user documentation
  - [ ] 3.2.1 Document new progress indicators
  - [ ] 3.2.2 Explain improved responsiveness
  - [ ] 3.2.3 Note any changes in behavior from previous version
