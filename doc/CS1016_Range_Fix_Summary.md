# CS1016 Range Fix Summary

## Problem

When selecting certain measurement ranges (specifically **1000 V** and **200 mV**), the multimeter beeps and shows a **"CSPI Execution Error"**. Other ranges work normally.

## Root Cause

The **CS1016 scanning card** has **different range limitations** than the SDM4055A multimeter itself. The application was allowing users to select ranges that are **NOT supported** by the CS1016 scanning card, which caused SCPI errors when the device tried to configure those ranges.

### Key Findings from CS1016 Datasheet

The CS1016 scanning card (used for multi-channel scanning) has significant range limitations compared to the standalone multimeter:

| Measurement Type | SDM4055A (Standalone) | CS1016 (Scanning) | Issue |
|-----------------|---------------------------|---------------------|---------|
| **Voltage** | 200 mV, 2 V, 20 V, 200 V, **1000 V** | 200 mV, 2 V, 20 V, **200 V** | **1000 V NOT supported** |
| **Voltage (AC)** | 200 mV, 2 V, 20 V, 200 V, **750 V** | 200 mV, 2 V, 20 V, **200 V** | **750 V NOT supported** |
| **Current (DC)** | 200 uA, 2 mA, 20 mA, 200 mA, 2 A, 10 A | **2 A ONLY** | **All other ranges NOT supported** |
| **Current (AC)** | 20 mA, 200 mA, 2 A, 10 A | **2 A ONLY** | **All other ranges NOT supported** |
| **Capacitance** | 2 nF, 20 nF, 200 nF, 2 uF, 20 uF, 200 uF, 2 mF, 20 mF, 100 mF | 2 nF, 20 nF, 200 nF, 2 uF, 20 uF, 200 uF, **10000 uF** | **2 mF, 20 mF, 100 mF NOT supported on SDM4055A** |

### Critical Limitations

1. **Voltage Maximum**: CS1016 only supports up to **200 V** (not 1000 V or 750 V)
   - Safety rating: 125V AC, 110V DC
   - Attempting to use 1000 V or 750 V causes SCPI error

2. **Current Range**: CS1016 **ONLY supports 2 A range**
   - Maximum continuous current: 2.2 A
   - All other current ranges (200 uA, 2 mA, 20 mA, 200 mA, 10 A, AUTO) are NOT supported
   - Attempting to use any other current range causes SCPI error

3. **Capacitance High Ranges**: 2 mF, 20 mF, 100 mF are only supported on SDM3065X, not SDM4055A
   - Alternative: Use **10000 uF** instead of 10 mF

## Solution Implemented

Updated the application to **prevent users from selecting unsupported ranges** by:

### 1. Updated GUI Range Options (`gui/widgets.py`)

Modified `VALID_RANGES`, `RANGE_TO_UNIT`, and `RANGE_TO_CONVERSION` dictionaries to only include CS1016-supported ranges:

```python
VALID_RANGES = {
    # Voltage ranges - CS1016 only supports up to 200V (1000V and 750V are NOT supported)
    "VOLT:DC": ["200 mV", "2 V", "20 V", "200 V", "AUTO"],
    "VOLT:AC": ["200 mV", "2 V", "20 V", "200 V", "AUTO"],
    # Current ranges - CS1016 ONLY supports 2A range (all other ranges are NOT supported)
    "CURR:DC": ["2 A"],  # Only 2A is supported by CS1016
    "CURR:AC": ["2 A"],  # Only 2A is supported by CS1016
    # Resistance ranges - All ranges supported
    "RES": ["200 Ohm", "2 kOhm", "20 kOhm", "200 kOhm", "2 MOhm", "10 MOhm", "100 MOhm", "AUTO"],
    "FRES": ["200 Ohm", "2 kOhm", "20 kOhm", "200 kOhm", "2 MOhm", "10 MOhm", "100 MOhm", "AUTO"],
    # Capacitance ranges - 2mF, 20mF, 100mF are NOT supported on SDM4055A (only SDM3065X)
    # Use 10000 uF as alternative to 10 mF
    "CAP": ["2 nF", "20 nF", "200 nF", "2 uF", "20 uF", "200 uF", "10000 uF", "AUTO"],
}
```

### 2. Updated VISA Interface (`hardware/visa_interface.py`)

Modified `RANGE_TO_SCPI` dictionary and `set_channel_range()` method to validate ranges based on CS1016 limitations:

```python
RANGE_TO_SCPI = {
    # Voltage ranges - CS1016 only supports up to 200V (1000V and 750V are NOT supported)
    "200 mV": "200mV",
    "2 V": "2V",
    "20 V": "20V",
    "200 V": "200V",
    # Current ranges - CS1016 ONLY supports 2A range (all other ranges are NOT supported)
    "2 A": "2A",
    # Capacitance ranges - 10000 uF is supported instead of 10 mF
    "2 nF": "2nF",
    "20 nF": "20nF",
    "200 nF": "200nF",
    "2 uF": "2uF",
    "20 uF": "20uF",
    "200 uF": "200uF",
    "10000 uF": "10000uF",
    # Resistance ranges
    "200 Ohm": "200OHM",
    "2 kOhm": "2kOHM",
    "20 kOhm": "20kOHM",
    "200 kOhm": "200kOHM",
    "2 MOhm": "2MOHM",
    "10 MOhm": "10MOHM",
    "100 MOhm": "100MOHM",
    # AUTO range
    "AUTO": "AUTO",
}
```

Added validation in `set_channel_range()` to check range compatibility with measurement type and log detailed error messages if invalid range is selected.

### 3. Updated Configuration Loader (`config/config_loader.py`)

Modified `VALID_RANGES` dictionary to only include CS1016-supported ranges and updated sample configuration file to use correct ranges.

### 4. Created Documentation (`doc/CS1016_Supported_Ranges.md`)

Comprehensive documentation file explaining:
- All supported ranges for each measurement type
- Channel capabilities (CH1-CH12 vs CH13-CH16)
- Safety specifications
- SCPI command examples
- Troubleshooting guide
- Comparison table: Multimeter vs CS1016 Scanning Card

## Files Modified

1. **`gui/widgets.py`**
   - Updated `VALID_RANGES` dictionary
   - Updated `RANGE_TO_UNIT` dictionary
   - Updated `RANGE_TO_CONVERSION` dictionary

2. **`hardware/visa_interface.py`**
   - Updated `RANGE_TO_SCPI` dictionary
   - Enhanced `set_channel_range()` method with CS1016 validation

3. **`config/config_loader.py`**
   - Updated `VALID_RANGES` dictionary
   - Updated sample configuration file examples

4. **`doc/CS1016_Supported_Ranges.md`** (NEW)
   - Comprehensive documentation of CS1016 supported ranges
   - Troubleshooting guide
   - Safety specifications

## Testing Recommendations

### Test Cases to Verify Fix

1. **Voltage Range Testing**
   - ✅ Select "200 mV" - Should work without error
   - ✅ Select "2 V" - Should work without error
   - ✅ Select "20 V" - Should work without error
   - ✅ Select "200 V" - Should work without error
   - ❌ Try to select "1000 V" - Should NOT be available in dropdown

2. **Current Range Testing** (Channels 13-16 only)
   - ✅ Select "2 A" - Should work without error
   - ❌ Try to select "200 uA" - Should NOT be available in dropdown
   - ❌ Try to select "2 mA" - Should NOT be available in dropdown
   - ❌ Try to select "20 mA" - Should NOT be available in dropdown
   - ❌ Try to select "200 mA" - Should NOT be available in dropdown
   - ❌ Try to select "10 A" - Should NOT be available in dropdown
   - ❌ Try to select "AUTO" - Should NOT be available in dropdown

3. **Capacitance Range Testing**
   - ✅ Select "10000 uF" - Should work without error
   - ❌ Try to select "2 mF" - Should NOT be available in dropdown
   - ❌ Try to select "20 mF" - Should NOT be available in dropdown
   - ❌ Try to select "100 mF" - Should NOT be available in dropdown

4. **Configuration File Loading**
   - Create a config file with unsupported ranges (e.g., 1000 V, 200 mA)
   - Attempt to load the file
   - ✅ Should receive validation error with detailed message explaining the issue

## Important Notes

### For Users

1. **Voltage Measurements**
   - Maximum supported range: **200 V**
   - For voltages above 200 V, use the multimeter in **standalone mode** (without scanning)

2. **Current Measurements**
   - **Only 2 A range is supported** when using CS1016 scanning card
   - For other current ranges, use the multimeter in **standalone mode** (without scanning)

3. **Configuration Files**
   - Ensure configuration files use only supported ranges
   - Use `doc/CS1016_Supported_Ranges.md` as reference for valid ranges

4. **Error Messages**
   - If you see "Invalid range" error, check the documentation for supported ranges
   - The error message will now include a list of valid ranges for the selected measurement type

### For Developers

1. **Range Validation**
   - All range validation is now centralized in `VALID_RANGES` dictionaries
   - Changes to supported ranges should be made in all three locations:
     - `gui/widgets.py` - `VALID_RANGES`, `RANGE_TO_UNIT`, `RANGE_TO_CONVERSION`
     - `hardware/visa_interface.py` - `RANGE_TO_SCPI`
     - `config/config_loader.py` - `VALID_RANGES`

2. **Documentation**
   - Always update `doc/CS1016_Supported_Ranges.md` when range support changes
   - Keep documentation in sync with code

## References

- **CS1016 Datasheet**: `doc/SC1016_Datasheet_DS60030-E02B.pdf`
- **CS1016 Supported Ranges**: `doc/CS1016_Supported_Ranges.md`
- **SCPI Commands Reference**: `doc/SCPI_Commands_Reference.md`
- **SDM4055A Programming Guide**: `doc/SDM-Series-Digital-Multimeter_ProgrammingGuide_EN02A.pdf`

## Conclusion

The issue was caused by the application allowing users to select ranges that are not supported by the CS1016 scanning card. By updating the validation to only allow CS1016-supported ranges, users will no longer encounter SCPI errors when selecting invalid ranges.

The fix ensures that:
- ✅ Users can only select supported ranges in the UI
- ✅ Configuration files are validated for supported ranges
- ✅ Detailed error messages guide users to correct ranges
- ✅ Documentation clearly explains all limitations
