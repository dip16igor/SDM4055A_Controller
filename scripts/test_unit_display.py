"""
Test script for dynamic unit display functionality.
Tests that units update correctly when measurement types change.
"""

import sys
from PySide6.QtWidgets import QApplication
from gui.widgets import ChannelIndicator

# Create QApplication instance once
app = QApplication(sys.argv)

def test_unit_mapping():
    """Test that all measurement types map to correct units."""
    print("Testing unit mapping...")
    
    # Define test cases with appropriate channel numbers
    test_cases = [
        # Voltage channel tests (channel 1)
        ("VOLT:DC", "V", 1),
        ("VOLT:AC", "V", 1),
        ("RES", "Ohm", 1),
        ("FRES", "Ohm", 1),
        ("CAP", "F", 1),
        ("FREQ", "Hz", 1),
        ("DIOD", "V", 1),
        ("CONT", "Ohm", 1),
        ("TEMP:RTD", "C", 1),
        ("TEMP:THER", "C", 1),
        # Current channel tests (channel 13)
        ("CURR:DC", "A", 13),
        ("CURR:AC", "A", 13),
    ]
    
    # Test each measurement type
    all_passed = True
    for measurement_type, expected_unit, channel_num in test_cases:
        indicator = ChannelIndicator(channel_num=channel_num)
        indicator.set_measurement_type(measurement_type)
        actual_unit = indicator.unit_label.text()
        
        if actual_unit == expected_unit:
            print(f"  [PASS] {measurement_type:15} -> {actual_unit}")
        else:
            print(f"  [FAIL] {measurement_type:15} -> Expected: {expected_unit}, Got: {actual_unit}")
            all_passed = False
    
    return all_passed

def test_default_units():
    """Test that default units are set correctly on initialization."""
    print("\nTesting default units...")
    
    # Test voltage channel (1-12)
    voltage_indicator = ChannelIndicator(channel_num=1)
    voltage_unit = voltage_indicator.unit_label.text()
    if voltage_unit == "V":
        print(f"  [PASS] Channel 1 (voltage) default unit: {voltage_unit}")
    else:
        print(f"  [FAIL] Channel 1 (voltage) default unit: Expected V, Got {voltage_unit}")
    
    # Test current channel (13-16)
    current_indicator = ChannelIndicator(channel_num=13)
    current_unit = current_indicator.unit_label.text()
    if current_unit == "A":
        print(f"  [PASS] Channel 13 (current) default unit: {current_unit}")
    else:
        print(f"  [FAIL] Channel 13 (current) default unit: Expected A, Got {current_unit}")
    
    return voltage_unit == "V" and current_unit == "A"

def test_unit_updates_on_change():
    """Test that units update when measurement type changes."""
    print("\nTesting unit updates on measurement type change...")
    
    indicator = ChannelIndicator(channel_num=1)
    
    # Start with voltage
    indicator.set_measurement_type("VOLT:DC")
    if indicator.unit_label.text() != "V":
        print(f"  [FAIL] Initial unit not set correctly")
        return False
    
    # Change to resistance
    indicator.set_measurement_type("RES")
    if indicator.unit_label.text() != "Ohm":
        print(f"  [FAIL] Unit not updated to Ohm")
        return False
    
    # Change to capacitance
    indicator.set_measurement_type("CAP")
    if indicator.unit_label.text() != "F":
        print(f"  [FAIL] Unit not updated to F")
        return False
    
    print(f"  [PASS] Units update correctly on measurement type change")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Dynamic Unit Display Test Suite")
    print("=" * 60)
    
    test1_passed = test_unit_mapping()
    test2_passed = test_default_units()
    test3_passed = test_unit_updates_on_change()
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    print(f"Unit Mapping Test:        {'PASSED' if test1_passed else 'FAILED'}")
    print(f"Default Units Test:       {'PASSED' if test2_passed else 'FAILED'}")
    print(f"Unit Updates Test:        {'PASSED' if test3_passed else 'FAILED'}")
    print("=" * 60)
    
    if test1_passed and test2_passed and test3_passed:
        print("\n[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Some tests failed!")
        sys.exit(1)
