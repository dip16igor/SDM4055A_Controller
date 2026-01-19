# AUTO Range Unit Display Implementation

## Overview
This document describes the implementation of unit information parsing from SCPI responses when using AUTO range.

## Problem
When the multimeter is configured to use AUTO range, it automatically selects the appropriate range based on the measured value. However, the SCPI response from `:ROUT:DATA? <channel>` returns the measurement value along with a unit suffix (e.g., "-4.24124300E-04 VDC"). This makes it impossible to know which range was actually used without parsing the unit information from the response.

## Solution
The `get_scan_data()` method in [`hardware/visa_interface.py`](hardware/visa_interface.py) has been updated to parse and return unit information from the SCPI response.

## Implementation Details

### 1. ScanDataResult Dataclass
A new dataclass [`ScanDataResult`](hardware/visa_interface.py:16-22) has been added to store unit information:

```python
@dataclass
class ScanDataResult:
    """Result from scanning a channel with unit information."""
    value: float
    unit: str  # Base unit (V, A, OHM, F, Hz, °C, etc.)
    full_unit: str  # Full unit string (VDC, VAC, ADC, AAC, OHM, etc.)
    range_info: str = ""  # Optional range information (e.g., "200mV", "2V", "AUTO")
```

### 2. Updated get_scan_data() Method
The [`get_scan_data()`](hardware/visa_interface.py:560-607) method now:

- Returns [`ScanDataResult`](hardware/visa_interface.py:16-17) instead of just `float`
- Parses the SCPI response to extract unit information
- Maps common unit suffixes to base units (e.g., "VDC" → "V", "ADC" → "A", "OHM" → "Ω")
- Returns `ScanDataResult`](hardware/visa_interface.py:16-17) with three fields:
  - `value`: The measurement value
  - `unit`: Base unit (V, A, Ω, F, Hz, °C, etc.)
  - `full_unit`: Full unit string (VDC, VAC, ADC, AAC, OHM, F, HZ, DEGC, DEGF, etc.)

### 3. Unit Mapping Logic
The method uses a mapping dictionary to convert full unit strings to base units:

```python
unit_mapping = {
    "VDC": "V", "VAC": "V",
    "ADC": "A", "AAC": "A",
    "OHM": "Ω", "OHMS": "Ω",
    "F": "F",
    "HZ": "Hz", "HERTZ": "Hz",
    "DEGC": "°C", "DEGF": "°F",
}
```

### 4. Example Usage
When reading scan data from a channel:

```python
result = visa_interface.get_scan_data(1)
if result:
    print(f"Value: {result.value}")
    print(f"Unit: {result.unit}")
    print(f"Full Unit: {result.full_unit}")
```

Example outputs:
- `Value: 1.23456789`, `Unit: V`, `Full Unit: VDC` (200 mV range)
- `Value: 12.3456789`, `Unit: V`, `Full Unit: VDC` (2 V range)
- `Value: 0.000123456`, `Unit: A`, `Full Unit: ADC` (current measurement)
```

### 5. Benefits
1. **Automatic unit detection**: The application can now automatically determine which unit was used
2. **Accurate display**: Users will see the correct unit symbol in the interface
3. **Better debugging**: Unit information is logged in debug mode
4. **Future-proof**: The structure supports additional range information if needed

### 6. Files Modified
- [`hardware/visa_interface.py`](hardware/visa_interface.py) - Added `ScanDataResult` dataclass and updated `get_scan_data()` method

## Next Steps
To fully utilize this feature, the GUI code needs to be updated to:
1. Import the `ScanDataResult` class from [`hardware/visa_interface.py`](hardware/visa_interface.py)
2. Update the display logic to extract and show the `unit` and `full_unit` fields from the result
3. Update logging to include unit information

## Testing
Test the implementation by running the application and checking the console output for unit information in debug mode.
