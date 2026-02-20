#!/usr/bin/env python3
"""
Test script to verify single threshold behavior in configuration.

This script tests that:
1. Only lower threshold: value must be >= lower_threshold to be GREEN
2. Only upper threshold: value must be <= upper_threshold to be GREEN
3. Both thresholds: value must be between them
4. No thresholds: always passes
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import config module
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config_loader import ChannelThresholdConfig


def test_lower_threshold_only():
    """Test that only lower threshold works correctly."""
    print("Testing lower threshold only...")
    
    # Create config with only lower threshold
    config = ChannelThresholdConfig(
        channel_num=1,
        name="Test",
        measurement_type="RES",
        range_value="AUTO",
        lower_threshold=100.0,
        upper_threshold=None
    )
    
    # Test values below threshold (should fail - RED)
    assert not config.is_value_in_threshold(50.0), "Value 50.0 should be below lower threshold 100.0"
    print("  [OK] Value 50.0 < 100.0 -> RED (correct)")
    
    # Test value at threshold (should pass - GREEN)
    assert config.is_value_in_threshold(100.0), "Value 100.0 should equal lower threshold"
    print("  [OK] Value 100.0 >= 100.0 -> GREEN (correct)")
    
    # Test value above threshold (should pass - GREEN)
    assert config.is_value_in_threshold(150.0), "Value 150.0 should be above lower threshold"
    print("  [OK] Value 150.0 >= 100.0 -> GREEN (correct)")
    
    print("[PASS] Lower threshold only: PASSED\n")


def test_upper_threshold_only():
    """Test that only upper threshold works correctly."""
    print("Testing upper threshold only...")
    
    # Create config with only upper threshold
    config = ChannelThresholdConfig(
        channel_num=1,
        name="Test",
        measurement_type="VOLT:DC",
        range_value="AUTO",
        lower_threshold=None,
        upper_threshold=5.0
    )
    
    # Test value below threshold (should pass - GREEN)
    assert config.is_value_in_threshold(3.0), "Value 3.0 should be below upper threshold"
    print("  [OK] Value 3.0 <= 5.0 -> GREEN (correct)")
    
    # Test value at threshold (should pass - GREEN)
    assert config.is_value_in_threshold(5.0), "Value 5.0 should equal upper threshold"
    print("  [OK] Value 5.0 <= 5.0 -> GREEN (correct)")
    
    # Test value above threshold (should fail - RED)
    assert not config.is_value_in_threshold(7.0), "Value 7.0 should be above upper threshold"
    print("  [OK] Value 7.0 > 5.0 -> RED (correct)")
    
    print("[PASS] Upper threshold only: PASSED\n")


def test_both_thresholds():
    """Test that both thresholds work correctly."""
    print("Testing both thresholds...")
    
    # Create config with both thresholds
    config = ChannelThresholdConfig(
        channel_num=1,
        name="Test",
        measurement_type="VOLT:DC",
        range_value="AUTO",
        lower_threshold=3.0,
        upper_threshold=5.0
    )
    
    # Test value below lower threshold (should fail - RED)
    assert not config.is_value_in_threshold(2.0), "Value 2.0 should be below lower threshold"
    print("  [OK] Value 2.0 < 3.0 -> RED (correct)")
    
    # Test value at lower threshold (should pass - GREEN)
    assert config.is_value_in_threshold(3.0), "Value 3.0 should equal lower threshold"
    print("  [OK] Value 3.0 >= 3.0 and <= 5.0 -> GREEN (correct)")
    
    # Test value in middle (should pass - GREEN)
    assert config.is_value_in_threshold(4.0), "Value 4.0 should be within thresholds"
    print("  [OK] Value 4.0 >= 3.0 and <= 5.0 -> GREEN (correct)")
    
    # Test value at upper threshold (should pass - GREEN)
    assert config.is_value_in_threshold(5.0), "Value 5.0 should equal upper threshold"
    print("  [OK] Value 5.0 >= 3.0 and <= 5.0 -> GREEN (correct)")
    
    # Test value above upper threshold (should fail - RED)
    assert not config.is_value_in_threshold(6.0), "Value 6.0 should be above upper threshold"
    print("  [OK] Value 6.0 > 5.0 -> RED (correct)")
    
    print("[PASS] Both thresholds: PASSED\n")


def test_no_thresholds():
    """Test that no thresholds always passes."""
    print("Testing no thresholds...")
    
    # Create config with no thresholds
    config = ChannelThresholdConfig(
        channel_num=1,
        name="Test",
        measurement_type="VOLT:DC",
        range_value="AUTO",
        lower_threshold=None,
        upper_threshold=None
    )
    
    # All values should pass
    assert config.is_value_in_threshold(-1000.0), "Any value should pass when no thresholds"
    assert config.is_value_in_threshold(0.0), "Any value should pass when no thresholds"
    assert config.is_value_in_threshold(1000.0), "Any value should pass when no thresholds"
    print("  [OK] All values pass when no thresholds set (correct)")
    
    print("[PASS] No thresholds: PASSED\n")


def main():
    """Run all threshold tests."""
    print("=" * 60)
    print("Single Threshold Behavior Test")
    print("=" * 60)
    print()
    
    try:
        test_lower_threshold_only()
        test_upper_threshold_only()
        test_both_thresholds()
        test_no_thresholds()
        
        print("=" * 60)
        print("[PASS] ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("Summary:")
        print("  • Only lower threshold: value must be >= lower_threshold")
        print("  • Only upper threshold: value must be <= upper_threshold")
        print("  • Both thresholds: value must be between them")
        print("  • No thresholds: always passes")
        print()
        
        return 0
        
    except AssertionError as e:
        print("=" * 60)
        print("[FAIL] TEST FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
