## 1. GUI Enhancements
- [x] 1.1 Add measurement type dropdown to ChannelIndicator widget
- [x] 1.2 Create enum or constant list of available measurement types for GUI
- [x] 1.3 Add signal to ChannelIndicator for measurement type changes
- [x] 1.4 Update ChannelIndicator layout to accommodate dropdown control
- [x] 1.5 Add method to ChannelIndicator to get/set current measurement type

## 2. Main Window Integration
- [x] 2.1 Connect channel measurement type change signals to main window
- [x] 2.2 Store per-channel measurement type configurations in MainWindow
- [x] 2.3 Create method to retrieve all channel measurement configurations
- [x] 2.4 Pass channel configurations to scan manager before scanning

## 3. Scan Manager Updates
- [x] 3.1 Update AsyncScanManager to accept channel configurations
- [x] 3.2 Configure device with per-channel measurement types before scan
- [x] 3.3 Ensure measurement types are applied in correct order before scan starts

## 4. Device Interface Updates
- [x] 4.1 Verify VisaInterface.set_channel_measurement_type works correctly
- [x] 4.2 Add method to configure all channels at once with their types
- [x] 4.3 Ensure thread-safe channel configuration

## 5. Testing
- [x] 5.1 Test measurement type selection for individual channels
- [x] 5.2 Test scan with different measurement types per channel
- [x] 5.3 Verify measurement types persist across scan cycles
- [x] 5.4 Test with simulator mode
- [x] 5.5 Test with real device if available
