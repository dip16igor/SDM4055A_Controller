# Debug Guide: 200 mV Range Issue

## Problem Description

When manually selecting "200 mV" range:
- ❌ Multimeter beeps and shows "CSPI Execution Error"
- ❌ Measurement fails

When selecting "AUTO" range:
- ✅ Multimeter automatically selects "Auto 200 mV" range
- ✅ Measurement works correctly

## Diagnostic Steps

### Step 1: Check Exact Error Message

Please provide the exact error message shown by the multimeter when you select "200 mV". This will help identify the root cause.

**What to do:**
1. Connect to multimeter
2. Select "200 mV" range for a channel
3. Try to start scanning
4. Note the exact error message displayed
5. Share the error message with me

**Possible Error Messages:**
- "CSPI Execution Error"
- "Invalid range"
- "Command error"
- "Parameter error"
- Other specific error code

### Step 2: Check Logs

Look at the application logs for detailed information about the SCPI command being sent:

**Log Location:**
- Check console output when you select "200 mV"
- Look for lines starting with "Configuring channel"
- Note the exact SCPI command being sent

**Expected Command for 200 mV:**
```
:ROUT:CHAN 1,ON,DCV,200mV,FAST
```

**Expected Command for AUTO:**
```
:ROUT:CHAN 1,ON,DCV,AUTO,FAST
```

### Step 3: Test Different Range Formats

The issue might be with the range format. Let's test different variations:

#### Format A: Without space (as per CS1016 datasheet)
```
:ROUT:CHAN 1,ON,DCV,200mV,FAST
```

#### Format B: With space (as per SCPI reference)
```
:ROUT:CHAN 1,ON,DCV,200 mV,FAST
```

#### Format C: Lowercase unit
```
:ROUT:CHAN 1,ON,DCV,200mv,FAST
```

#### Format D: With quotes
```
:ROUT:CHAN 1,ON,DCV,"200mV",FAST
```

### Step 4: Test Other Ranges

Test if other ranges work correctly:

**Voltage Ranges:**
- ✅ AUTO (should work)
- ❓ 2 V (test this)
- ❓ 20 V (test this)
- ❓ 200 V (test this)

**Current Ranges (channels 13-16 only):**
- ✅ 2 A (should work)

### Step 5: Check Device Response

When the error occurs, check if the device returns any response:

1. Open a terminal or command prompt
2. Connect to the multimeter manually using VISA
3. Send the command: `:ROUT:CHAN 1,ON,DCV,200mV,FAST`
4. Query the device status: `:SYST:ERR?`
5. Note the error code and message

Example error query:
```bash
:SYST:ERR?
```

Expected response format:
```
-113,"Undefined header"
```

Or:
```
0,"No error"
```

### Step 6: Check CS1016 Documentation

Review the CS1016 datasheet for exact command syntax:

**Key Points to Verify:**
1. Is the range parameter format correct?
2. Are there any additional parameters required?
3. Is the order of parameters correct?
4. Are there any special characters or delimiters?

**From CS1016 Datasheet Table 3:**
Available ranges for DCV/ACV/FRQ:
- Auto, 200mV, 2V, 20V, 200V

**Note:** The datasheet shows "200mV" (without space), not "200 mV" (with space).

### Step 7: Test with Different Multimeter Models

If possible, test with:
- SDM3055-SC (if available)
- SDM3065X-SC (if available)

Different models might have different command implementations.

### Step 8: Check for Firmware Updates

Check if there are any firmware updates available for the CS1016 scanning card that might fix range command issues.

### Step 9: Test Sequential Channel Configuration

Try configuring channels one by one instead of using scan mode:

1. Set measurement function: `:CONF:VOLT:DC`
2. Set range: `:CONF:VOLT:DC 200mV`
3. Read measurement: `:MEAS:VOLT:DC?`

This bypasses the CS1016 scanning card and uses the main multimeter functions directly.

## Temporary Workaround

While we debug the issue, you can use the following workaround:

### Option 1: Use AUTO Range
- Select "AUTO" instead of "200 mV"
- The multimeter will automatically select the appropriate range

### Option 2: Use Standalone Mode
- If you need to use specific ranges like 200 mV:
  1. Disable scanning mode
  2. Configure the channel directly using CONF commands
  3. Use MEAS commands to read values

### Option 3: Use Different Range
- If 200 mV doesn't work, try using 2 V range instead
- The 2 V range is also supported and should work

## Information Needed for Debugging

To help resolve this issue, please provide:

1. **Exact error message** when selecting 200 mV
2. **Device model** (SDM4055A-SC or other)
3. **Firmware version** (from `*IDN?` command)
4. **Log output** showing the SCPI command being sent
5. **Whether other ranges** (2 V, 20 V, 200 V) work correctly
6. **Whether the issue occurs** on all channels or only specific ones

## Next Steps

Once you provide the diagnostic information, I can:

1. Identify the exact cause of the error
2. Implement a fix in the code
3. Test the fix with your device
4. Update documentation

## Code Changes Made

### Added Delay Between Channel Configurations

**File:** `hardware/visa_interface.py`
**Method:** [`configure_all_scan_channels()`](hardware/visa_interface.py:421)
**Change:** Increased delay from 0.1s to 1.0s between channel configurations

**Before:**
```python
time.sleep(0.1)  # 100ms delay between channels
```

**After:**
```python
time.sleep(1.0)  # 1 second delay between channels for device to settle
```

**Rationale:** The CS1016 scanning card may need additional time to settle between channel configuration changes, especially when switching ranges. A longer delay helps prevent timing issues that could cause SCPI errors.

## Testing the Fix

After updating to the latest code, please test:

1. **Test 200 mV Range:**
   - Select "200 mV" for a channel
   - Start scanning
   - Check if error still occurs

2. **Test AUTO Range:**
   - Select "AUTO" for a channel
   - Start scanning
   - Verify it works correctly

3. **Test Other Ranges:**
   - Test 2 V, 20 V, 200 V ranges
   - Verify all work correctly

4. **Check Logs:**
   - Look for "Configuring channel" messages
   - Verify 1-second delay is applied between channels
   - Check for any error messages

## Contact Information

If the issue persists after trying all diagnostic steps, please contact:
- Siglent Technical Support
- Check for firmware updates
- Verify CS1016 card compatibility

---

**Last Updated:** 2026-01-16
**Status:** Added 1-second delay between channel configurations. Awaiting user testing feedback.
