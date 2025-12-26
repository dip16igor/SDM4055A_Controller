## 1. Hardware Layer Updates
- [x] 1.1 Add multi-channel support to VISA interface with CS1016 card commands
- [x] 1.2 Implement channel switching logic for 16 channels
- [x] 1.3 Add measurement type configuration methods (voltage, resistance, capacitance, frequency, diode, temperature, current)
- [x] 1.4 Implement multi-channel read operation that cycles through all channels
- [x] 1.5 Add error handling for channel switching failures

## 2. GUI Components
- [x] 2.1 Create modern digital indicator widget with unit label display
- [x] 2.2 Implement channel configuration dropdown for measurement type selection
- [x] 2.3 Create START/STOP scanning buttons with proper state management
- [x] 2.4 Implement scan interval slider (1s-10s range, default 2s)
- [x] 2.5 Add USB device address display at top of interface
- [x] 2.6 Create 16-channel grid layout with proper spacing and sizing

## 3. Main Window Integration
- [x] 3.1 Update main window to display all 16 channels in grid layout
- [x] 3.2 Add measurement type selection UI for channels 1-12 (voltage, resistance, capacitance, frequency, diode, temperature)
- [x] 3.3 Add AC/DC selection UI for channels 13-16 (current only)
- [x] 3.4 Implement START/STOP button handlers for scanning control
- [x] 3.5 Connect scan interval slider to polling timer
- [x] 3.6 Update connection status display with USB device address

## 4. Scanning Logic
- [x] 4.1 Implement multi-channel scanning timer with configurable interval
- [x] 4.2 Add channel cycling logic to read all channels sequentially
- [x] 4.3 Store and update measurement values for all channels
- [x] 4.4 Handle scanning state (running/stopped) properly
- [x] 4.5 Add error handling for communication failures during scanning

## 5. Testing and Validation
- [x] 5.1 Test multi-channel scanning with simulator mode
- [x] 5.2 Verify all measurement types work correctly
- [x] 5.3 Test scan interval slider functionality
- [x] 5.4 Validate START/STOP controls
- [x] 5.5 Test with real CS1016 card if available
