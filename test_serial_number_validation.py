"""Test script for serial number validation."""
import re

def validate_serial_number(text: str) -> bool:
    """Validate serial number format: PSN followed by exactly 9 digits.
    
    Args:
        text: Serial number string to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    pattern = r'^PSN\d{9}$'
    return bool(re.match(pattern, text))

# Test cases
test_cases = [
    # Valid cases
    ("PSN123456789", True, "Valid: PSN + 9 digits"),
    ("PSN000000000", True, "Valid: PSN + 9 zeros"),
    ("PSN999999999", True, "Valid: PSN + 9 nines"),
    
    # Invalid cases - missing prefix
    ("123456789", False, "Invalid: Missing PSN prefix"),
    ("SN123456789", False, "Invalid: Wrong prefix (SN instead of PSN)"),
    ("psn123456789", False, "Invalid: Lowercase prefix"),
    
    # Invalid cases - wrong digit count
    ("PSN12345678", False, "Invalid: Only 8 digits"),
    ("PSN1234567890", False, "Invalid: 10 digits"),
    ("PSN12345", False, "Invalid: Only 6 digits"),
    
    # Invalid cases - contains non-digit characters
    ("PSN1234567A", False, "Invalid: Contains letter at end"),
    ("PSN12345678!", False, "Invalid: Contains special character"),
    ("PSN1234567 9", False, "Invalid: Contains space"),
    
    # Edge cases
    ("", False, "Invalid: Empty string"),
    ("PSN", False, "Invalid: Only prefix, no digits"),
    ("PSN123456789 ", False, "Invalid: Trailing space"),
    (" PSN123456789", False, "Invalid: Leading space"),
]

print("Serial Number Validation Tests")
print("=" * 60)

passed = 0
failed = 0

for serial, expected, description in test_cases:
    result = validate_serial_number(serial)
    status = "PASS" if result == expected else "FAIL"
    
    if result == expected:
        passed += 1
    else:
        failed += 1
    
    print(f"{status}: {description}")
    print(f"       Input: '{serial}'")
    print(f"       Expected: {expected}, Got: {result}")
    print()

print("=" * 60)
print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")

if failed == 0:
    print("All tests passed!")
else:
    print(f"WARNING: {failed} test(s) failed!")
