# Change: Compact Value Display with Inline Units

## Why
The current UI layout displays measurement units on a separate line below the measured value, which takes up unnecessary vertical space and makes the interface less compact. Additionally, the current measurement value font size (36pt) still appears small on some displays, especially when viewing multiple channels simultaneously.

Moving units inline with the measured value will:
- Reduce vertical space usage, allowing more content to fit on screen
- Make the interface cleaner and more modern
- Improve readability by keeping value and unit together as a single visual element
- Allow for larger font sizes within the same vertical space

Increasing the font size will:
- Improve readability from a distance
- Make measurements easier to read at a glance
- Enhance accessibility for users with visual impairments

## What Changes
- Move unit display from separate label to inline with measured value (e.g., "5.001619 V" instead of value on one line and "V" on the next)
- Increase measurement value font size from 36pt to 48pt for better readability
- Adjust layout to accommodate inline unit display
- Maintain threshold-based color coding functionality
- Preserve all existing functionality (measurement types, ranges, thresholds, etc.)

## Impact
- Affected specs: multimeter-controller
- Modified files:
  - `gui/widgets.py` - Update ChannelIndicator layout and font sizing

## Technical Details
The `ChannelIndicator` widget currently uses:
- `value_label` (36pt font) for displaying the numeric value
- `unit_label` (12pt font) on a separate line for displaying units

Changes will:
1. Remove the separate `unit_label` widget
2. Modify `value_label` to include the unit inline (e.g., `f"{value:.6f} {unit}"`)
3. Increase `value_label` font size from 36pt to 48pt
4. Update `set_value()` method to include unit in the text
5. Remove or simplify `set_unit()` method as units will be part of value display
6. Adjust vertical spacing in the layout to accommodate larger font

The `DigitalIndicator` widget already displays units inline (line 92 in current code) and can serve as a reference for the implementation approach.
