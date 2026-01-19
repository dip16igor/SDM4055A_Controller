## 1. ChannelIndicator Layout Updates
- [ ] 1.1 Remove separate unit_label widget from ChannelIndicator
- [ ] 1.2 Remove unit_label from layout in _setup_ui method
- [ ] 1.3 Adjust vertical spacing in layout to accommodate larger font
- [ ] 1.4 Remove unit_label initialization in __init__ method

## 2. Value Display Updates
- [ ] 2.1 Increase value_label font size from 36pt to 48pt in _setup_ui
- [ ] 2.2 Update set_value method to include unit inline with value
- [ ] 2.3 Modify value text format to include unit (e.g., f"{value:.6f} {unit}")
- [ ] 2.4 Update set_status method to maintain error/success status display
- [ ] 2.5 Update reset_status method to restore value with unit

## 3. Unit Management Updates
- [ ] 3.1 Simplify set_unit method to just update internal _unit variable
- [ ] 3.2 Remove unit_label.setText call from set_unit
- [ ] 3.3 Update _update_unit_for_measurement_type to trigger value refresh
- [ ] 3.4 Ensure unit updates trigger set_value to refresh display

## 4. Testing
- [ ] 4.1 Test inline unit display with various measurement types (VOLT:DC, VOLT:AC, CURR:DC, CURR:AC, RES, CAP, FREQ)
- [ ] 4.2 Test inline unit display with different ranges (AUTO and fixed ranges)
- [ ] 4.3 Verify threshold color coding still works with inline units
- [ ] 4.4 Test value display with long unit strings (e.g., "kOhm", "MOhm")
- [ ] 4.5 Verify larger font size (48pt) displays correctly
- [ ] 4.6 Test layout with multiple channels to ensure compactness
- [ ] 4.7 Test status display (error messages, "Disconnected") still works
- [ ] 4.8 Verify no text overflow or clipping with larger font
- [ ] 4.9 Test dynamic unit updates when changing measurement types
- [ ] 4.10 Test dynamic unit updates when changing ranges
