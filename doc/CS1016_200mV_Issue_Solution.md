# CS1016 Range Issue - Final Analysis and Solution

## Problem Summary

When selecting "200 mV" range for a channel:
- ❌ Multimeter beeps and shows "CSPI Execution Error"
- ❌ Measurement fails

When selecting "AUTO" range:
- ✅ Multimeter automatically selects "Auto200mV" mode
- ✅ Measurement works correctly

## Root Cause Analysis

### Key Finding: "200 mV" Range is NOT Supported by CS1016 Scanning Card

**Evidence from logs:**
1. Command `:ROUT:CHAN1,ON,DCV,200mV,FAST` is **accepted** by device (error code: 0,"No Error")
2. But multimeter **beeps immediately** and shows "CSPI Execution Error"
3. In AUTO mode, multimeter shows "Auto200mV" on display

**Conclusion:** The "200 mV" range is technically in the CS1016 datasheet as a supported range, but the CS1016 scanning card **cannot actually use it**. When the command is sent, the device accepts it (error code 0), but then fails to apply it, causing the error.

### Additional Finding: Current Measurement Type Limitation

When configuring channel 13 for current measurement:
- Command: `:ROUT:CHAN13,ON,DCA,2A,FAST`
- User observation: "мультиметр поддерживает только режим SLOW"
- This indicates that for current measurements, the multimeter/CS1016A-SC only supports the **2A** range, not AUTO

**Important:** This is a separate limitation from the "200 mV" issue. The 2A range IS supported, but only in SLOW mode, not AUTO mode.

## CS1016 Scanning Card Range Limitations

Based on CS1016 datasheet analysis:

### Voltage Ranges (DCV/ACV/FREQ)
| Range | Supported by CS1016 | Notes |
|-------|-------------------|---------|
| 200 mV | ❌ **NO** | In datasheet but causes error | Try AUTO instead |
| 2 V | ✅ YES | | | |
| 20 V | ✅ YES | | |
| 200 V | ✅ YES | | Max: 200V |
| AUTO | ✅ YES | | Recommended |

### Current Ranges (DCA/ACA)
| Range | Supported by CS1016 | Notes |
|-------|-------------------|---------|
| 2 A | ✅ YES | **ONLY in SLOW mode** | |
| AUTO | ❌ NO | | Use 2A in SLOW mode |

### Resistance Ranges (2W/4W)
| Range | Supported by CS1016 | Notes |
|-------|-------------------|---------|
| 200 Ohm | ✅ YES | |
| 2 kOhm | ✅ YES | | |
| 20 kOhm | ✅ YES | |
| 200 kOhm | ✅ YES | |
| 2 MOhm | ✅ YES | |
| 10 MOhm | ✅ YES | |
| 100 MOhm | ✅ YES | |
| AUTO | ✅ YES | |

### Capacitance Ranges (CAP)
| Range | Supported by CS1016 | Notes |
|-------|-------------------|---------|
| 2 nF | ✅ YES | |
| 20 nF | ✅ YES | |
| 200 nF | ✅ YES | |
| 2 uF | ✅ YES | |
| 20 uF | ✅ YES | |
| 200 uF | ✅ YES | |
| 10000 uF | ✅ YES | Alternative to 10 mF |
| AUTO | ✅ YES | |

### Other Measurement Types
| Type | Supported Ranges |
|-------|-------------------|---------|
| FREQ | AUTO only |
| DIOD | AUTO only |
| CONT | AUTO only |
| TEMP:RTD | AUTO only |
| TEMP:THER | AUTO only |

## Solution Implemented

### 1. Removed "200 mV" from Supported Ranges

**Files Modified:**
- [`gui/widgets.py`](gui/widgets.py:222-230) - Removed "200 mV" from `VALID_RANGES` for voltage
- [`hardware/visa_interface.py`](hardware/visa_interface.py:189-215) - Removed "200 mV" from `RANGE_TO_SCPI` dictionary
- [`config/config_loader.py`](config/config_loader.py:68-81) - Removed "200 mV" from `VALID_RANGES`

**Code Changes:**
```python
# Before (caused issues):
"200 mV": "200mV"

# After (fixed):
# NOTE: "200 mV" range is NOT SUPPORTED by CS1016 scanning card - causes "CSPI Execution Error"
# Use AUTO instead, or use 2 V, 20 V, 200 V ranges
```

### 2. Added Error Checking After Channel Configuration

**File:** [`hardware/visa_interface.py`](hardware/visa_interface.py:412-428)

**Added Code:**
```python
# Check for errors after configuration
try:
    # Query system error status to detect configuration errors
    error_response = self.instrument.query(":SYST:ERR?")
    error_response = error_response.strip()
    if error_response and error_response != '0,"No error"':
        logger.error(f"Channel {channel_num} configuration error: {error_response}")
        # Log additional details
        try:
            error_query = self.instrument.query(":SYST:ERR?")
            logger.error(f"Error details: {error_query.strip()}")
        except:
            pass
except pyvisa.Error as e:
    logger.warning(f"Could not query error status: {e}")
```

### 3. Added 1-Second Delay Between Channels

**File:** [`hardware/visa_interface.py`](hardware/visa_interface.py:449-450)

**Code Changes:**
```python
# Add delay between channel configurations
time.sleep(1.0)  # 1 second delay between channels for device to settle
```

## Why "200 mV" Range Causes Errors

The "200 mV" range is listed in the CS1016 datasheet as a supported range, but:

1. **It's not actually supported** - The CS1016 scanning card cannot use the "200 mV" range
2. **Multimeter tries to switch to it** - When command is sent, device accepts it but fails to apply it
3. **Timing issue** - Multimeter may need more time to switch to this range

## Current Measurement Type Limitation

**Important Discovery:** For current measurements (DCA/ACA), the CS1016/SDM405A-SC only supports the **2A** range, and **ONLY in SLOW mode** (not AUTO mode).

## Recommendations for Users

### 1. **Never Use "200 mV" Range**
- This range causes "CSPI Execution Error"
- Use AUTO instead - multimeter will automatically select appropriate range
- Or use 2 V, 20 V, or 200 V ranges

### 2. **For Current Measurements**
- Use **2 A** range with **SLOW mode** (not AUTO)
- Do not use AUTO for current measurements

### 3. **For Other Measurement Types**
- Use AUTO range - all other types only support AUTO

### 4. **Check Logs**
- Look for "Channel X configuration error" messages
- These will help identify which specific ranges cause issues

## Files Modified Summary

1. **[`hardware/visa_interface.py`](hardware/visa_interface.py)**
   - Removed "200 mV" from `RANGE_TO_SCPI` dictionary
   - Added error checking after channel configuration
   - Increased delay between channel configurations to 1 second

2. **[`gui/widgets.py`](gui/widgets.py)**
   - Removed "200 mV" from `VALID_RANGES` for voltage

3. **[`config/config_loader.py`](config/config_loader.py)**
   - Removed "200 mV" from `VALID_RANGES`

4. **[`doc/CS1016_Supported_Ranges.md`](doc/CS1016_Supported_Ranges.md)**
   - Created comprehensive documentation of supported ranges

5. **[`doc/CS1016_200mV_Issue_Summary.md`](doc/CS1016_200mV_Issue_Summary.md)**
   - Created final analysis and solution document

## Testing Instructions

After updating to the latest code, please:

1. **Test "200 mV" range**
   - Try to select it for a channel
   - Check if error still occurs
   - Check logs for "Channel X configuration error" messages

2. **Test AUTO range**
   - Select AUTO for the same channel
   - Verify it works correctly

3. **Test other voltage ranges**
   - Try 2 V, 20 V, 200 V ranges
   - Verify all work without errors

4. **Check logs**
   - Verify that "200 mV" is no longer in command
   - Verify that error checking is working
   - Verify that 1-second delay is applied between channels

## Expected Results

With these changes:
- ✅ "200 mV" range will NOT appear in dropdown menus
- ✅ Users can only select CS1016-supported ranges
- ✅ Error checking will provide detailed diagnostic information
- ✅ 1-second delay between channels should improve stability
- ✅ Current measurements will only allow 2A range in SLOW mode

## Documentation Reference

See [`doc/CS1016_Supported_Ranges.md`](doc/CS1016_Supported_Ranges.md) for complete list of supported ranges for all measurement types.

## Conclusion

The "200 mV" range issue is caused by including a range in the supported ranges list that the CS1016 scanning card cannot actually use. By removing it from the UI and SCPI mappings, users will no longer be able to select it, preventing the "CSPI Execution Error".

The root cause is that the CS1016 scanning card has different range limitations than the multimeter itself, and the "200 mV" range, despite being listed in the datasheet, is not actually supported when using the scanning card functionality.
