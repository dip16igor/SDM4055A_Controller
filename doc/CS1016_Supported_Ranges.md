# CS1016 Scanning Card - Supported Ranges

## Overview

The CS1016 scanning card has **different range limitations** compared to the SDM4055A multimeter itself. When using the scanning card (channels 1-16), only specific ranges are supported.

## Critical Findings

The CS1016 scanning card does NOT support all ranges that the multimeter supports in standalone mode. This is why you're getting "CSPI Execution Error" when selecting certain ranges like **1000 V** or **200 mV**.

## Supported Ranges by Measurement Type

### Voltage (DCV/ACV/Frequency)

**Channels 1-12 only** (CH13-CH16 are for current only)

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| 200 mV | ✅ **YES** | Supported |
| 2 V | ✅ **YES** | Supported |
| 20 V | ✅ **YES** | Supported |
| 200 V | ✅ **YES** | Supported |
| 1000 V | ❌ **NO** | **NOT SUPPORTED** - Will cause SCPI Error |
| 750 V | ❌ **NO** | **NOT SUPPORTED** - Will cause SCPI Error |
| AUTO | ✅ **YES** | Supported |

**Important Notes:**
- Maximum voltage for CS1016: **125V AC, 110V DC** (per safety specifications)
- The 1000 V and 750 V ranges are **NOT supported** by the CS1016 scanning card
- If you need to measure voltages above 200V, use the multimeter in standalone mode (without scanning)

### Current (DCI/ACI)

**Channels 13-16 only** (CH1-CH12 do not support current)

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| 200 uA | ❌ **NO** | **NOT SUPPORTED** - Will cause SCPI Error |
| 2 mA | ❌ **NO** | **NOT SUPPORTED** - Will cause SCPI Error |
| 20 mA | ❌ **NO** | **NOT SUPPORTED** - Will cause SCPI Error |
| 200 mA | ❌ **NO** | **NOT SUPPORTED** - Will cause SCPI Error |
| 2 A | ✅ **YES** | **ONLY SUPPORTED RANGE** |
| 10 A | ❌ **NO** | **NOT SUPPORTED** - Will cause SCPI Error |
| AUTO | ❌ **NO** | **NOT SUPPORTED** - Will cause SCPI Error |

**Critical Limitation:**
- The CS1016 scanning card **ONLY supports the 2 A range** for current measurements
- All other current ranges (200 uA, 2 mA, 20 mA, 200 mA, 10 A, AUTO) are **NOT supported**
- **Current measurements MUST use SLOW speed** (FAST speed is not supported for current)
- Maximum continuous current: **2.2 A** (per safety specifications)

### Resistance (2W/4W)

**Channels 1-12 only**

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| 200 Ohm | ✅ **YES** | Supported |
| 2 kOhm | ✅ **YES** | Supported |
| 20 kOhm | ✅ **YES** | Supported |
| 200 kOhm | ✅ **YES** | Supported |
| 2 MOhm | ✅ **YES** | Supported (1 MOhm for SDM3065X) |
| 10 MOhm | ✅ **YES** | Supported |
| 100 MOhm | ✅ **YES** | Supported |
| AUTO | ✅ **YES** | Supported |

### Capacitance (CAP)

**Channels 1-12 only**

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| 2 nF | ✅ **YES** | Supported |
| 20 nF | ✅ **YES** | Supported |
| 200 nF | ✅ **YES** | Supported |
| 2 uF | ✅ **YES** | Supported |
| 20 uF | ✅ **YES** | Supported |
| 200 uF | ✅ **YES** | Supported |
| 2 mF | ❌ **NO** | **NOT SUPPORTED** on SDM4055A (only SDM3065X) |
| 20 mF | ❌ **NO** | **NOT SUPPORTED** on SDM4055A (only SDM3065X) |
| 100 mF | ❌ **NO** | **NOT SUPPORTED** on SDM4055A (only SDM3065X) |
| 10000 uF | ✅ **YES** | Alternative to 10 mF |
| AUTO | ✅ **YES** | Supported |

**Note:** The 2 mF, 20 mF, and 100 mF ranges are only supported on SDM3065X, not on SDM4055A.

### Frequency (FREQ)

**Channels 1-12 only**

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| AUTO | ✅ **YES** | Supported |
| 200 mV | ✅ **YES** | Same ranges as DCV/ACV |
| 2 V | ✅ **YES** | Same ranges as DCV/ACV |
| 20 V | ✅ **YES** | Same ranges as DCV/ACV |
| 200 V | ✅ **YES** | Same ranges as DCV/ACV |

### Diode Test (DIOD)

**Channels 1-12 only**

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| AUTO | ✅ **YES** | Supported (fixed range) |

### Continuity Test (CONT)

**Channels 1-12 only**

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| AUTO | ✅ **YES** | Supported (fixed range 2 kOhm) |

### Temperature (RTD)

**Channels 1-12 only**

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| AUTO | ✅ **YES** | Supported |

### Temperature (Thermocouple)

**Channels 1-12 only**

| Range | Supported by CS1016 | Notes |
|-------|-------------------|-------|
| AUTO | ✅ **YES** | Supported |

## Channel Capabilities Summary

| Channels | Supported Functions | Notes |
|----------|---------------------|-------|
| CH1-CH12 | DCV, ACV, 2WR, 4WR, CAP, FREQ, DIOD, CONT, TEMP (RTD & Thermocouple) | Multi-purpose channels |
| CH13-CH16 | DCI, ACI (2A range ONLY) | Current-only channels |

## Safety Specifications

| Parameter | Maximum Rating |
|-----------|----------------|
| AC Voltage | 125V rms or 175V peak, 100kHz, 0.3A switched, 125VA (resistive load) |
| DC Voltage | 110V, 1A switched, 30VDC (resistive load) |
| Continuous Current (CH13-CH16) | < 2.2A |
| Contact Life | > 100,000 operations at 1A 30VDC or 0.3A 125VDC |
| Contact Resistance | 75 mΩ (maximum at 6VDC, 1A) |
| Actuation Time | 5ms maximum on/off |
| Maximum Switching Voltage | 250 VAC, 220 VDC |
| Maximum Switching Power | 62.5VA / 30W |
| Insulation Resistance | Minimum 1 GΩ (500VDC) |

## SCPI Commands

When configuring channels for scanning, use the following format:

```
:ROUT:CHAN <ch>,ON,<type>,<range>,<speed>
```

Where:
- `<ch>`: Channel number (1-16)
- `<type>`: Measurement type (DCV, ACV, DCI, ACI, RES, CAP, FREQ, DIOD, CONT, RTD, THER)
- `<range>`: Range value from the supported ranges above
- `<speed>`: Measurement speed (FAST or SLOW - current measurements MUST use SLOW)

### Examples

**Correct usage (supported ranges):**
```
:ROUT:CHAN 1,ON,DCV,200mV,FAST
:ROUT:CHAN 1,ON,DCV,2V,FAST
:ROUT:CHAN 1,ON,DCV,20V,FAST
:ROUT:CHAN 1,ON,DCV,200V,FAST
:ROUT:CHAN 13,ON,DCI,2A,SLOW      # DC Current MUST use SLOW speed
:ROUT:CHAN 14,ON,ACI,2A,SLOW      # AC Current MUST use SLOW speed
```

**Incorrect usage (unsupported ranges - will cause SCPI Error):**
```
:ROUT:CHAN 1,ON,DCV,1000V,FAST    ❌ NOT SUPPORTED
:ROUT:CHAN 1,ON,DCV,750V,FAST     ❌ NOT SUPPORTED
:ROUT:CHAN 13,ON,DCA,10A,FAST     ❌ NOT SUPPORTED (only 2A)
:ROUT:CHAN 13,ON,DCA,200mA,FAST   ❌ NOT SUPPORTED (only 2A)
```

## Troubleshooting

### Problem: "CSPI Execution Error" when selecting range

**Cause:** You're trying to use a range that is not supported by the CS1016 scanning card.

**Solution:** Use only the supported ranges listed above for each measurement type.

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| 1000 V range error | CS1016 does not support 1000 V | Use 200 V max or AUTO |
| 750 V range error | CS1016 does not support 750 V | Use 200 V max or AUTO |
| 200 mV range error | Should work - check command format | Verify SCPI command format: `200mV` (not `200 mV`) |
| Current range errors (except 2A) | CS1016 only supports 2A range | Use 2A range for current measurements |
| Current measurement errors | Current MUST use SLOW speed | Use SLOW speed for current measurements (DCA/ACA) |
| 2 mF, 20 mF, 100 mF errors | Not supported on SDM4055A | Use 10000 uF or AUTO instead |

## Comparison: Multimeter vs CS1016 Scanning Card

### Voltage Ranges

| Range | SDM4055A (Standalone) | CS1016 (Scanning) |
|-------|----------------------|-------------------|
| 200 mV | ✅ | ✅ |
| 2 V | ✅ | ✅ |
| 20 V | ✅ | ✅ |
| 200 V | ✅ | ✅ |
| 1000 V | ✅ | ❌ **NOT SUPPORTED** |
| 750 V (AC) | ✅ | ❌ **NOT SUPPORTED** |

### Current Ranges

| Range | SDM4055A (Standalone) | CS1016 (Scanning) |
|-------|----------------------|-------------------|
| 200 uA | ✅ | ❌ **NOT SUPPORTED** |
| 2 mA | ✅ | ❌ **NOT SUPPORTED** |
| 20 mA | ✅ | ❌ **NOT SUPPORTED** |
| 200 mA | ✅ | ❌ **NOT SUPPORTED** |
| 2 A | ✅ | ✅ **ONLY SUPPORTED RANGE** |
| 10 A | ✅ | ❌ **NOT SUPPORTED** |

## Recommendations

1. **For Voltage Measurements:**
   - Use CS1016 for voltages up to 200V
   - For voltages above 200V, use the multimeter in standalone mode

2. **For Current Measurements:**
   - CS1016 only supports 2A range
   - **Current measurements MUST use SLOW speed** (not FAST)
   - For other current ranges, use the multimeter in standalone mode

3. **For High-Precision Measurements:**
   - Use 4-wire resistance for better accuracy
   - Use AUTO range when unsure of the expected value

4. **For Safety:**
   - Always respect the maximum ratings (125V AC, 110V DC, 2.2A continuous)
   - Never exceed the specified limits to avoid damage to the equipment

## References

- SC1016 Datasheet: https://www.siglenteu.com/wp-content/uploads/dlm_uploads/2022/01/SC1016_Datasheet_DS60030-E02B.pdf
- SDM4055A Programming Guide: doc/SDM-Series-Digital-Multimeter_ProgrammingGuide_EN02A.pdf
- SCPI Commands Reference: doc/SCPI_Commands_Reference.md
