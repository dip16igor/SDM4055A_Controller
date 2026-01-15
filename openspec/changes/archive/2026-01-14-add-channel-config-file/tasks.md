## 1. Implementation
- [x] 1.1 Create config package with __init__.py
- [x] 1.2 Implement ConfigLoader class in config/config_loader.py
- [x] 1.3 Implement ChannelThresholdConfig dataclass
- [x] 1.4 Add CSV parsing with comment support
- [x] 1.5 Add validation for channel numbers (1-16)
- [x] 1.6 Add validation for measurement types per channel
- [x] 1.7 Add validation for threshold values
- [x] 1.8 Add comprehensive error messages for validation failures

## 2. GUI Updates
- [x] 2.1 Add ConfigLoader instance to MainWindow
- [x] 2.2 Add "Load Config" button to Scan Control section
- [x] 2.3 Add label to display loaded configuration file name
- [x] 2.4 Implement _on_load_config_clicked handler
- [x] 2.5 Add file dialog for selecting CSV files
- [x] 2.6 Implement _apply_configuration method
- [x] 2.7 Update UI to show config file status

## 3. Channel Indicator Updates
- [x] 3.1 Add threshold attributes to ChannelIndicator
- [x] 3.2 Implement set_thresholds method
- [x] 3.3 Implement clear_thresholds method
- [x] 3.4 Implement _apply_threshold_color method
- [x] 3.5 Update set_value to apply threshold colors
- [x] 3.6 Test green color for values within thresholds
- [x] 3.7 Test red color for values outside thresholds
- [x] 3.8 Add threshold display label to ChannelIndicator
- [x] 3.9 Implement _update_thresholds_display method
- [x] 3.10 Increase measurement value font size from 28pt to 36pt
- [x] 3.11 Test threshold display with various configurations

## 4. Testing
- [x] 4.1 Create sample_config.csv with example configurations
- [x] 4.2 Test loading valid configuration file
- [x] 4.3 Test loading invalid configuration files (various error cases)
- [x] 4.4 Test partial channel configuration
- [x] 4.5 Test threshold validation logic
- [x] 4.6 Test color coding with different measurement values
- [x] 4.7 Verify GUI integration with file loading
