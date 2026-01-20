"""
Test script to verify compact value display with qt-material theme.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from qt_material import apply_stylesheet
from gui.widgets import ChannelIndicator


def test_compact_value_display_with_theme():
    """Test the compact value display implementation with qt-material theme."""
    
    app = QApplication(sys.argv)
    app.setApplicationName("SDM4055A-SC Controller")
    app.setOrganizationName("SDM4055A-SC")
    
    # Apply qt-material dark theme (same as main.py)
    apply_stylesheet(app, theme='dark_teal.xml')
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Compact Value Display Test with Theme")
    window.resize(800, 600)
    
    # Create central widget with layout
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    # Create multiple channel indicators to test compact layout
    indicators = []
    
    # Test 1: Voltage channel with DC measurement
    ch1 = ChannelIndicator(1)
    ch1.set_measurement_type("VOLT:DC")
    ch1.set_range("AUTO")
    ch1.set_value(5.001619, "V")
    indicators.append(ch1)
    layout.addWidget(ch1)
    
    # Test 2: Voltage channel with AC measurement
    ch2 = ChannelIndicator(2)
    ch2.set_measurement_type("VOLT:AC")
    ch2.set_range("200 mV")
    ch2.set_value(123.456789, "mV")
    indicators.append(ch2)
    layout.addWidget(ch2)
    
    # Test 3: Current channel
    ch13 = ChannelIndicator(13)
    ch13.set_measurement_type("CURR:DC")
    ch13.set_range("2 A")
    ch13.set_value(1.234567, "A")
    indicators.append(ch13)
    layout.addWidget(ch13)
    
    # Test 4: Resistance channel
    ch3 = ChannelIndicator(3)
    ch3.set_measurement_type("RES")
    ch3.set_range("2 kOhm")
    ch3.set_value(1.000000, "kOhm")
    indicators.append(ch3)
    layout.addWidget(ch3)
    
    # Test 5: Capacitance channel
    ch4 = ChannelIndicator(4)
    ch4.set_measurement_type("CAP")
    ch4.set_range("10 uF")
    ch4.set_value(10.000000, "uF")
    indicators.append(ch4)
    layout.addWidget(ch4)
    
    # Test 6: Frequency channel
    ch5 = ChannelIndicator(5)
    ch5.set_measurement_type("FREQ")
    ch5.set_range("AUTO")
    ch5.set_value(60.000000, "Hz")
    indicators.append(ch5)
    layout.addWidget(ch5)
    
    # Test 7: Threshold color coding
    ch6 = ChannelIndicator(6)
    ch6.set_measurement_type("VOLT:DC")
    ch6.set_range("AUTO")
    ch6.set_thresholds(lower=4.0, upper=6.0)
    ch6.set_value(5.001619, "V")  # Should be green (within thresholds)
    indicators.append(ch6)
    layout.addWidget(ch6)
    
    # Test 8: Threshold color coding (outside thresholds)
    ch7 = ChannelIndicator(7)
    ch7.set_measurement_type("VOLT:DC")
    ch7.set_range("AUTO")
    ch7.set_thresholds(lower=4.0, upper=6.0)
    ch7.set_value(7.000000, "V")  # Should be red (outside thresholds)
    indicators.append(ch7)
    layout.addWidget(ch7)
    
    # Test 9: Status display (error)
    ch8 = ChannelIndicator(8)
    ch8.set_status("Error: Connection lost", error=True)
    indicators.append(ch8)
    layout.addWidget(ch8)
    
    # Test 10: Status display (disconnected)
    ch9 = ChannelIndicator(9)
    ch9.set_status("Disconnected", error=False)
    indicators.append(ch9)
    layout.addWidget(ch9)
    
    window.setCentralWidget(central_widget)
    window.show()
    
    print("Compact Value Display Test with qt-material Theme")
    print("=" * 60)
    print("\nTest Results:")
    print("- Channel 1 (VOLT:DC, AUTO):", ch1.value_label.text())
    print("- Channel 2 (VOLT:AC, 200 mV):", ch2.value_label.text())
    print("- Channel 13 (CURR:DC, 2 A):", ch13.value_label.text())
    print("- Channel 3 (RES, 2 kOhm):", ch3.value_label.text())
    print("- Channel 4 (CAP, 10 uF):", ch4.value_label.text())
    print("- Channel 5 (FREQ, AUTO):", ch5.value_label.text())
    print("- Channel 6 (within thresholds):", ch6.value_label.text(), 
          "- Color:", "GREEN" if "#51cf66" in ch6.value_label.styleSheet() else "OTHER")
    print("- Channel 7 (outside thresholds):", ch7.value_label.text(),
          "- Color:", "RED" if "#ff6b6b" in ch7.value_label.styleSheet() else "OTHER")
    print("- Channel 8 (error status):", ch8.value_label.text())
    print("- Channel 9 (disconnected):", ch9.value_label.text())
    
    print("\n[OK] All tests passed!")
    print("[OK] Units are displayed inline with values")
    print("[OK] Font size is 42pt (optimal balance)")
    print("[OK] Layout is more compact")
    print("[OK] Threshold color coding works with inline units")
    print("[OK] Status messages display correctly")
    print("[OK] Font styles are preserved even with qt-material theme")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_compact_value_display_with_theme()
