"""
Test script to verify ChannelIndicator.set_status fix.
This tests that the set_status method works correctly after fixing the status_label bug.
"""
import sys
from PySide6.QtWidgets import QApplication
from gui.widgets import ChannelIndicator

def test_set_status():
    """Test the set_status method of ChannelIndicator."""
    print("Testing ChannelIndicator.set_status method...")
    print("=" * 60)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create a ChannelIndicator
    indicator = ChannelIndicator(channel_num=1)
    
    # Test 1: Set status without error
    print("\nTest 1: Set status without error")
    try:
        indicator.set_status("Test Status", error=False)
        print("[PASS] set_status('Test Status', error=False) succeeded")
        print(f"  Value label text: '{indicator.value_label.text()}'")
    except AttributeError as e:
        print(f"[FAIL] {e}")
        return False
    
    # Test 2: Set status with error
    print("\nTest 2: Set status with error")
    try:
        indicator.set_status("Error Status", error=True)
        print("[PASS] set_status('Error Status', error=True) succeeded")
        print(f"  Value label text: '{indicator.value_label.text()}'")
    except AttributeError as e:
        print(f"[FAIL] {e}")
        return False
    
    # Test 3: Set status with OVERLOAD text
    print("\nTest 3: Set status with OVERLOAD")
    try:
        indicator.set_status("OVERLOAD", error=True)
        print("[PASS] set_status('OVERLOAD', error=True) succeeded")
        print(f"  Value label text: '{indicator.value_label.text()}'")
    except AttributeError as e:
        print(f"[FAIL] {e}")
        return False
    
    # Test 4: Set status with "No data"
    print("\nTest 4: Set status with 'No data'")
    try:
        indicator.set_status("No data", error=True)
        print("[PASS] set_status('No data', error=True) succeeded")
        print(f"  Value label text: '{indicator.value_label.text()}'")
    except AttributeError as e:
        print(f"[FAIL] {e}")
        return False
    
    print("\n" + "=" * 60)
    print("All tests PASSED!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_set_status()
    sys.exit(0 if success else 1)
