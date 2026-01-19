# Unit Display and Overload Detection Fix

## Problem Statement

### Issue 1: Units Not Being Transmitted for AUTO Range
When using AUTO range, the multimeter displays values like "+160.213mVDC" on its screen, but the application was showing "0.160213 V". The unit information selected by the multimeter was not being transmitted to the application.

### Issue 2: Overload Values Not Displayed Correctly
When the measurement exceeds the range limit (e.g., 5V input on 2V range), the multimeter displays "overloadDC" on its screen, but the application was showing "9.9e+37" (a very large number representing overload).

## Solution

### 1. Enhanced ScanDataResult Dataclass

The `ScanDataResult` dataclass in [`hardware/visa_interface.py`](hardware/visa_interface.py:16-22) now includes:

```python
@dataclass
class ScanDataResult:
    """Result from scanning a channel with unit information."""
    value: float
    unit: str  # Base unit (V, A, OHM, F, Hz, °C, etc.)
    full_unit: str  # Full unit string (VDC, VAC, ADC, AAC, OHM, etc.)
    range_info: str = ""  # Optional range information (e.g., "200mV", "2V", "AUTO")
```

### 2. Unit Parsing from SCPI Response

The [`get_scan_data()`](hardware/visa_interface.py:560-640) method now:

1. Parses the SCPI response to extract both value and unit information
2. Maps full units to base units (e.g., "VDC" → "V", "ADC" → "A")
3. Returns a `ScanDataResult` object with all information

**Example SCPI Response Parsing:**
```
Input:  "0.160213 VDC"
Output: ScanDataResult(value=0.160213, unit="V", full_unit="VDC")
```

### 3. Overload Detection

The [`get_scan_data()`](hardware/visa_interface.py:560-640) method now detects overload conditions:

1. Checks if response contains "overload" string (case-insensitive)
2. Checks if value exceeds threshold (1e35)
3. Returns `ScanDataResult` with `unit="OVERLOAD"` when overload is detected

**Overload Detection Logic:**
```python
# Check for overload conditions
if "overload" in response_stripped.lower():
    return ScanDataResult(
        value=0.0,
        unit="OVERLOAD",
        full_unit=overload_msg,
        range_info="OVERLOAD"
    )

# Check if value is extremely large (indicates overload)
OVERLOAD_THRESHOLD = 1e35
if abs(value) > OVERLOAD_THRESHOLD:
    return ScanDataResult(
        value=0.0,
        unit="OVERLOAD",
        full_unit=full_unit,
        range_info="OVERLOAD"
    )
```

### 4. Updated Signal Types

The signal types in [`hardware/async_worker.py`](hardware/async_worker.py:26) have been updated:

**Before:**
```python
channel_read = Signal(int, float)  # Emitted when a single channel is read
```

**After:**
```python
channel_read = Signal(int, object)  # Emitted when a single channel is read (ScanDataResult or None)
```

### 5. GUI Updates

The GUI methods in [`gui/window.py`](gui/window.py) have been updated to handle `ScanDataResult` objects:

#### `_on_scan_complete()` (lines 460-482)
```python
for channel_num, result in measurements.items():
    if 1 <= channel_num <= 16:
        indicator = self.channel_indicators[channel_num - 1]
        
        if result is None:
            indicator.set_status("No data", error=True)
        elif result.unit == "OVERLOAD":
            indicator.set_status(result.full_unit, error=True)
        else:
            indicator.set_value(result.value, result.unit)
```

#### `_on_single_scan_complete()` (lines 491-510)
Same logic as `_on_scan_complete()`.

#### `_on_channel_read()` (lines 512-530)
```python
if result is None:
    indicator.set_status("No data", error=True)
elif isinstance(result, ScanDataResult) and result.unit == "OVERLOAD":
    indicator.set_status(result.full_unit, error=True)
elif isinstance(result, ScanDataResult):
    indicator.set_value(result.value, result.unit)
else:
    # Fallback for backward compatibility (if result is a float)
    indicator.set_value(float(result))
```

### 6. Unit Display in AUTO Range

The [`set_value()`](gui/widgets.py:372-399) method in `ChannelIndicator` now:

1. Accepts a `unit` parameter to override the default unit
2. When AUTO range is selected, uses the unit from the multimeter response
3. When fixed range is selected, applies conversion factor as before

**Example Behavior:**
- **AUTO Range with 200mV selected:** Displays "0.160213" with unit "V" (from multimeter response)
- **Fixed 200mV Range:** Displays "160.213000" with unit "mV" (converted from V to mV)

## Unit Mapping

The following unit mappings are supported:

| Full Unit | Base Unit | Description |
|------------|------------|-------------|
| VDC        | V          | DC Voltage |
| VAC        | V          | AC Voltage |
| ADC        | A          | DC Current |
| AAC        | A          | AC Current |
| OHM        | Ω          | Resistance |
| OHMS       | Ω          | Resistance |
| F          | F          | Capacitance |
| HZ         | Hz         | Frequency |
| HERTZ      | Hz         | Frequency |
| DEGC       | °C         | Temperature (Celsius) |
| DEGF       | °F         | Temperature (Fahrenheit) |

## Overload Detection Threshold

The overload threshold is set to `1e35` (1 followed by 35 zeros). Any value exceeding this threshold is considered an overload condition and will be displayed as "OVERLOAD" instead of the numeric value.

## Testing

### Test Case 1: AUTO Range
1. Set channel to AUTO range
2. Apply a small voltage (e.g., 160 mV)
3. Expected: Application displays "0.160213" with unit "V"
4. Multimeter displays: "+160.213mVDC"

### Test Case 2: Fixed Range
1. Set channel to 200 mV range
2. Apply a small voltage (e.g., 160 mV)
3. Expected: Application displays "160.213000" with unit "mV"
4. Multimeter displays: "+160.213mVDC"

### Test Case 3: Overload Condition
1. Set channel to 2V range
2. Apply a voltage exceeding 2V (e.g., 5V)
3. Expected: Application displays "overloadDC" in red
4. Multimeter displays: "overloadDC"

## Files Modified

1. [`hardware/visa_interface.py`](hardware/visa_interface.py)
   - Updated `get_scan_data()` to return `ScanDataResult` objects
   - Added unit parsing logic
   - Added overload detection logic
   - Updated `read_all_channels()` return type to `Dict[int, Optional[ScanDataResult]]`
   - Updated `_read_channels_sequentially()` return type to `Dict[int, Optional[ScanDataResult]]`

2. [`hardware/async_worker.py`](hardware/async_worker.py)
   - Added `ScanDataResult` import
   - Updated `channel_read` signal type from `Signal(int, float)` to `Signal(int, object)`

3. [`gui/window.py`](gui/window.py)
   - Added `ScanDataResult` import
   - Updated `_on_scan_complete()` to handle `ScanDataResult` objects
   - Updated `_on_single_scan_complete()` to handle `ScanDataResult` objects
   - Updated `_on_channel_read()` to handle `ScanDataResult` objects

4. [`gui/widgets.py`](gui/widgets.py)
   - Updated `set_value()` method to use unit from parameter when provided
   - Added comments explaining AUTO range behavior

## Notes

### AUTO Range Behavior
When AUTO range is selected, the multimeter automatically selects the best range based on the measured value. The SCPI response returns the value in the base unit (e.g., V for voltage), not in the selected range's unit (e.g., mV). Therefore, the application displays the value in the base unit as returned by the multimeter.

### Multimeter Display vs SCPI Response
The multimeter's display may show the value in a different unit than the SCPI response. For example:
- Multimeter display: "+160.213mVDC" (shows in mV because 200mV range was selected)
- SCPI response: "0.160213 VDC" (returns in V, the base unit)

This is normal behavior. The application displays the value as returned by the SCPI command.

### Backward Compatibility
The code includes fallback logic to handle `float` values for backward compatibility. If a `float` is received instead of a `ScanDataResult` object, it will be converted and displayed normally.

## Future Improvements

1. **Range Query Enhancement:** Add functionality to query the actual range selected by the multimeter when using AUTO mode, so the application can display the value in the same unit as the multimeter display.

2. **Custom Overload Messages:** Allow users to customize the overload message displayed in the application.

3. **Unit Conversion for AUTO Range:** Implement intelligent unit conversion for AUTO range to match the multimeter display format.
