# Implementation Tasks

## 1. Add ConfigLoader Methods
- [ ] 1.1 Add `get_min_channel()` method to return minimum configured channel number
- [ ] 1.2 Add `get_max_channel()` method to return maximum configured channel number
- [ ] 1.3 Add `is_channel_configured(channel_num)` method to check if channel is in config
- [ ] 1.4 Handle edge case when no config is loaded (return None or default values)

## 2. Modify VisaInterface Scanning Logic
- [ ] 2.1 Update `read_all_channels()` to accept optional config_loader parameter
- [ ] 2.2 Calculate scan range from config (min to max channel numbers)
- [ ] 2.3 Use `set_scan_limits(low, high)` with config-based values
- [ ] 2.4 Maintain backward compatibility: scan all channels (1-16) when no config provided
- [ ] 2.5 Update `configure_all_scan_channels()` to only configure channels in range
- [ ] 2.6 Update data reading loop to only read channels in configured range

## 3. Update GUI Channel Display
- [ ] 3.1 Modify `ChannelIndicator` widget to accept "configured" state
- [ ] 3.2 Apply gray color styling to unconfigured channel indicators
- [ ] 3.3 Update channel indicator initialization to check config status
- [ ] 3.4 Ensure gray color works in both light and dark themes

## 4. Integrate Config-Based Scanning in MainWindow
- [ ] 4.1 Pass config_loader instance to scanning methods
- [ ] 4.2 Update channel indicator display when config is loaded/unloaded
- [ ] 4.3 Refresh channel indicator states on config file load
- [ ] 4.4 Handle config unload (reset to scan all channels)

## 5. Testing
- [ ] 5.1 Test scanning with config containing channels 1, 3, 5 (should scan 1-5)
- [ ] 5.2 Test scanning with config containing channels 10, 13, 16 (should scan 10-16)
- [ ] 5.3 Test scanning without config (should scan all 1-16)
- [ ] 5.4 Test GUI display shows unconfigured channels in gray
- [ ] 5.5 Test config unload resets channel display to normal
- [ ] 5.6 Verify scan performance improvement with smaller channel ranges

## 6. Documentation
- [ ] 6.1 Update SCPI command reference documentation if needed
- [ ] 6.2 Add comments explaining config-based scanning logic
- [ ] 6.3 Update user documentation about channel range behavior
