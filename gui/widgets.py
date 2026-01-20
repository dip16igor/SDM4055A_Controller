"""
Custom GUI widgets for SDM4055A-SC multimeter controller.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QComboBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPalette, QColor
from typing import Optional


class DigitalIndicator(QWidget):
    """
    Card-style digital indicator widget for displaying measurement values.
    Features shadow effects and modern design.
    """

    value_changed = Signal(float)  # Signal emitted when value changes

    def __init__(self, title: str = "Measurement", parent=None):
        """
        Initialize digital indicator.

        Args:
            title: Title displayed above the value.
            parent: Parent widget.
        """
        super().__init__(parent)

        self._value = 0.0
        self._title = title

        # Setup UI
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the widget's UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Title label
        self.title_label = QLabel(self._title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)

        # Value label
        self.value_label = QLabel("0.0000 V")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_font = QFont()
        value_font.setPointSize(32)
        value_font.setBold(True)
        value_font.setFamily("Consolas, Courier New, monospace")
        self.value_label.setFont(value_font)
        layout.addWidget(self.value_label)

        # Status label
        self.status_label = QLabel("Disconnected")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_font = QFont()
        status_font.setPointSize(10)
        self.status_label.setFont(status_font)
        layout.addWidget(self.status_label)

        # Apply card style
        self._apply_card_style()

    def _apply_card_style(self) -> None:
        """Apply card-style appearance with shadow effects."""
        self.setStyleSheet("""
            DigitalIndicator {
                background-color: #2d2d2d;
                border-radius: 10px;
                border: 1px solid #3d3d3d;
            }
        """)

    def set_value(self, value: float, unit: str = "V") -> None:
        """
        Update the displayed value.

        Args:
            value: New measurement value.
            unit: Unit string to display.
        """
        self._value = value
        self.value_label.setText(f"{value:.6f} {unit}")
        self.value_changed.emit(value)

    def set_title(self, title: str) -> None:
        """
        Update the title.

        Args:
            title: New title string.
        """
        self._title = title
        self.title_label.setText(title)

    def set_status(self, status: str, error: bool = False) -> None:
        """
        Update the status label.

        Args:
            status: Status text to display.
            error: If True, display status in red color.
        """
        self.status_label.setText(status)
        if error:
            self.status_label.setStyleSheet("color: #ff6b6b;")
        else:
            self.status_label.setStyleSheet("color: #51cf66;")

    def get_value(self) -> float:
        """Get current displayed value."""
        return self._value


class ChannelIndicator(QWidget):
    """
    Channel indicator widget for displaying measurements from a single channel.
    Includes channel number, value display, unit label, and measurement type selector.
    """

    # Font size constants for easy customization
    VALUE_FONT_SIZE = 14 # Size of measurement value font (in points)
    
    measurement_type_changed = Signal(int, str)  # Signal emitted when measurement type changes (channel_num, type)
    range_changed = Signal(int, str)  # Signal emitted when range changes (channel_num, range_value)

    # Mapping of measurement types to display units
    MEASUREMENT_TYPE_TO_UNIT = {
        "VOLT:DC": "V",
        "VOLT:AC": "V",
        "CURR:DC": "A",
        "CURR:AC": "A",
        "RES": "Ohm",
        "FRES": "Ohm",
        "CAP": "F",
        "FREQ": "Hz",
        "DIOD": "V",
        "CONT": "Ohm",
        "TEMP:RTD": "C",
        "TEMP:THER": "C"
    }

    # Mapping of ranges to display units for each measurement type (CS1016 supported ranges only)
    RANGE_TO_UNIT = {
        # Voltage ranges (CS1016 only supports up to 200V)
        "200 mV": "mV",
        "2 V": "V",
        "20 V": "V",
        "200 V": "V",
        # Current ranges (CS1016 only supports 2A)
        "2 A": "A",
        # Capacitance ranges (CS1016 supports 10000 uF instead of 10 mF)
        "2 nF": "nF",
        "20 nF": "nF",
        "200 nF": "nF",
        "2 uF": "uF",
        "20 uF": "uF",
        "200 uF": "uF",
        "10000 uF": "uF",
        # Resistance ranges
        "200 Ohm": "Ohm",
        "2 kOhm": "kOhm",
        "20 kOhm": "kOhm",
        "200 kOhm": "kOhm",
        "2 MOhm": "MOhm",
        "10 MOhm": "MOhm",
        "100 MOhm": "MOhm",
    }

    # Mapping of ranges to value conversion factors (device returns values in base units)
    # CS1016 supported ranges only
    RANGE_TO_CONVERSION = {
        # Voltage ranges (device returns V)
        "200 mV": 1000,  # Convert V to mV (multiply by 1000)
        "2 V": 1,        # No conversion (V to V)
        "20 V": 1,       # No conversion (V to V)
        "200 V": 1,      # No conversion (V to V)
        # Current ranges (device returns A) - CS1016 only supports 2A
        "2 A": 1,         # No conversion (A to A)
        # Capacitance ranges (device returns F) - CS1016 supports 10000 uF instead of 10 mF
        "2 nF": 1e9,     # Convert F to nF (multiply by 1,000,000,000)
        "20 nF": 1e9,    # Convert F to nF (multiply by 1,000,000,000)
        "200 nF": 1e9,   # Convert F to nF (multiply by 1,000,000,000)
        "2 uF": 1e6,     # Convert F to uF (multiply by 1,000,000)
        "20 uF": 1e6,    # Convert F to uF (multiply by 1,000,000)
        "200 uF": 1e6,   # Convert F to uF (multiply by 1,000,000)
        "10000 uF": 1e6,  # Convert F to uF (multiply by 1,000,000)
        # Resistance ranges (device returns Ohm)
        "200 Ohm": 1,     # No conversion (Ohm to Ohm)
        "2 kOhm": 1e-3,  # Convert Ohm to kOhm (multiply by 0.001)
        "20 kOhm": 1e-3, # Convert Ohm to kOhm (multiply by 0.001)
        "200 kOhm": 1e-3, # Convert Ohm to kOhm (multiply by 0.001)
        "2 MOhm": 1e-6,  # Convert Ohm to MOhm (multiply by 0.000001)
        "10 MOhm": 1e-6,  # Convert Ohm to MOhm (multiply by 0.000001)
        "100 MOhm": 1e-6, # Convert Ohm to MOhm (multiply by 0.000001)
    }

    # Valid ranges for each measurement type (CS1016 scanning card limitations)
    # IMPORTANT: CS1016 scanning card has DIFFERENT range limitations than the multimeter itself!
    # See doc/CS1016_Supported_Ranges.md for detailed information
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

    def __init__(self, channel_num: int, parent=None):
        """
        Initialize channel indicator.

        Args:
            channel_num: Channel number (1-16).
            parent: Parent widget.
        """
        super().__init__(parent)

        self._channel_num = channel_num
        self._value = 0.0
        self._is_current_channel = channel_num > 12
        self._range_value = "AUTO"  # Default range
        
        # Set default unit based on channel type
        if self._is_current_channel:
            self._unit = "A"  # Current channels (13-16)
        else:
            self._unit = "V"  # Voltage/resistance channels (1-12)
        
        # Threshold configuration
        self._lower_threshold = None
        self._upper_threshold = None
        self._thresholds_enabled = False

        # Setup UI
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the widget's UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # Channel number label
        self.channel_label = QLabel(f"CH {self._channel_num}")
        self.channel_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        channel_font = QFont()
        channel_font.setPointSize(14)
        channel_font.setBold(True)
        self.channel_label.setFont(channel_font)
        layout.addWidget(self.channel_label)

        # Value label (large, readable with inline unit)
        self.value_label = QLabel("0.0000 V")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_font = QFont()
        value_font.setPointSize(self.VALUE_FONT_SIZE)
        value_font.setBold(True)
        value_font.setFamily("Consolas, Courier New, monospace")
        self.value_label.setFont(value_font)
        # Apply font via stylesheet to override theme defaults
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: {self.VALUE_FONT_SIZE}pt;
                font-weight: bold;
                font-family: 'Consolas', 'Courier New', monospace;
            }}
        """)
        layout.addWidget(self.value_label)
        
        # Thresholds label (displayed when thresholds are configured)
        self.thresholds_label = QLabel("")
        self.thresholds_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thresholds_font = QFont()
        thresholds_font.setPointSize(9)
        thresholds_font.setItalic(True)
        self.thresholds_label.setFont(thresholds_font)
        self.thresholds_label.setStyleSheet("color: #888;")
        layout.addWidget(self.thresholds_label)

        # Measurement type and range selector in horizontal layout
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        
        # Measurement type selector
        if self._is_current_channel:
            # Current channels (13-16): only AC/DC selection
            self.measurement_combo = QComboBox()
            self.measurement_combo.addItem("DC Current", "CURR:DC")
            self.measurement_combo.addItem("AC Current", "CURR:AC")
            self.measurement_combo.currentIndexChanged.connect(self._on_measurement_type_changed)
            controls_layout.addWidget(self.measurement_combo, stretch=1)
        else:
            # Voltage/resistance/capacitance channels (1-12): full selection
            self.measurement_combo = QComboBox()
            self.measurement_combo.addItem("DC Voltage", "VOLT:DC")
            self.measurement_combo.addItem("AC Voltage", "VOLT:AC")
            self.measurement_combo.addItem("2-Wire Resistance", "RES")
            self.measurement_combo.addItem("4-Wire Resistance", "FRES")
            self.measurement_combo.addItem("Capacitance", "CAP")
            self.measurement_combo.addItem("Frequency", "FREQ")
            self.measurement_combo.addItem("Diode", "DIOD")
            self.measurement_combo.addItem("Continuity", "CONT")
            self.measurement_combo.addItem("RTD Temperature", "TEMP:RTD")
            self.measurement_combo.addItem("Thermocouple", "TEMP:THER")
            self.measurement_combo.currentIndexChanged.connect(self._on_measurement_type_changed)
            controls_layout.addWidget(self.measurement_combo, stretch=1)
        
        # Range selector
        self.range_combo = QComboBox()
        self.range_combo.addItem("AUTO", "AUTO")
        self.range_combo.currentIndexChanged.connect(self._on_range_changed)
        controls_layout.addWidget(self.range_combo, stretch=1)
        
        # Add controls layout to main layout
        layout.addLayout(controls_layout)

        # Apply card style
        self._apply_card_style()

    def _apply_card_style(self) -> None:
        """Apply card-style appearance with shadow effects."""
        self.setStyleSheet("""
            ChannelIndicator {
                background-color: #2d2d2d;
                border-radius: 10px;
                border: 1px solid #3d3d3d;
            }
            QComboBox {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                min-height: 25px;
            }
            QComboBox:hover {
                background-color: #4d4d4d;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #3d3d3d;
                color: #ffffff;
                selection-background-color: #4a9eff;
                border: 1px solid #4d4d4d;
            }
        """)

    def set_value(self, value: float, unit: str = None) -> None:
        """
        Update the displayed value with range-based conversion and threshold color coding.

        Args:
            value: New measurement value (from device).
            unit: Unit string to display (optional, uses current unit if not provided).
        """
        self._value = value
        if unit is not None:
            self._unit = unit
        
        # Apply range-based value conversion
        range_value = self.range_combo.currentData()
        if range_value and range_value != "AUTO":
            # For fixed ranges, apply conversion factor
            conversion_factor = self.RANGE_TO_CONVERSION.get(range_value, 1)
            converted_value = value * conversion_factor
            self.value_label.setText(f"{converted_value:.6f} {self._unit}")
        else:
            # For AUTO range, use the unit from the device response
            # The device returns the value in the unit it selected (e.g., mV, V, etc.)
            self.value_label.setText(f"{value:.6f} {self._unit}")
        
        # Apply threshold-based color coding if enabled
        if self._thresholds_enabled:
            if range_value and range_value != "AUTO":
                self._apply_threshold_color(converted_value, use_converted=True)
            else:
                self._apply_threshold_color(value, use_converted=False)

    def set_unit(self, unit: str) -> None:
        """
        Update the unit and refresh the value display.

        Args:
            unit: Unit string to display.
        """
        self._unit = unit
        # Refresh value display with new unit
        self.set_value(self._value)

    def set_status(self, status: str, error: bool = False) -> None:
        """
        Update the channel status (displayed in value label).

        Args:
            status: Status text to display.
            error: If True, display status in red color.
        """
        self.value_label.setText(status)
        if error:
            self.value_label.setStyleSheet(f"""
                color: #ff6b6b;
                font-size: {self.VALUE_FONT_SIZE}pt;
                font-weight: bold;
                font-family: 'Consolas', 'Courier New', monospace;
            """)
        else:
            self.value_label.setStyleSheet(f"""
                color: #51cf66;
                font-size: {self.VALUE_FONT_SIZE}pt;
                font-weight: bold;
                font-family: 'Consolas', 'Courier New', monospace;
            """)

    def reset_status(self) -> None:
        """Reset the value label to normal display."""
        self.value_label.setText(f"{self._value:.6f} {self._unit}")
        self.value_label.setStyleSheet(f"""
            font-size: {self.VALUE_FONT_SIZE}pt;
            font-weight: bold;
            font-family: 'Consolas', 'Courier New', monospace;
        """)
    
    def set_thresholds(self, lower: Optional[float] = None, upper: Optional[float] = None) -> None:
        """
        Set threshold values for this channel.
        
        Args:
            lower: Lower threshold value (None to disable).
            upper: Upper threshold value (None to disable).
        """
        self._lower_threshold = lower
        self._upper_threshold = upper
        self._thresholds_enabled = (lower is not None) or (upper is not None)
        
        # Update thresholds display
        self._update_thresholds_display()
        
        # Re-apply color coding if thresholds are enabled
        if self._thresholds_enabled:
            self._apply_threshold_color(self._value)
    
    def clear_thresholds(self) -> None:
        """Clear threshold settings and reset color."""
        self._lower_threshold = None
        self._upper_threshold = None
        self._thresholds_enabled = False
        self.value_label.setStyleSheet("")
        self._update_thresholds_display()
    
    def _update_thresholds_display(self) -> None:
        """Update the thresholds label based on current threshold values."""
        if not self._thresholds_enabled:
            self.thresholds_label.setText("")
            return
        
        # Build threshold display text
        parts = []
        if self._lower_threshold is not None:
            parts.append(f">={self._lower_threshold:.6f}")
        if self._upper_threshold is not None:
            parts.append(f"<={self._upper_threshold:.6f}")
        
        if parts:
            self.thresholds_label.setText(" | ".join(parts))
        else:
            self.thresholds_label.setText("")
    
    def _apply_threshold_color(self, value: float = None, use_converted: bool = False) -> None:
        """
        Apply color based on threshold comparison.
        
        Args:
            value: The value to check against thresholds (original or converted).
            use_converted: If True, use converted value for comparison.
        """
        if not self._thresholds_enabled:
            return
        
        # Check if value is within thresholds
        in_range = True
        
        if self._lower_threshold is not None and value < self._lower_threshold:
            in_range = False
        
        if self._upper_threshold is not None and value > self._upper_threshold:
            in_range = False
        
        # Apply color while preserving font style
        if in_range:
            self.value_label.setStyleSheet(f"""
                color: #51cf66;
                font-size: {self.VALUE_FONT_SIZE}pt;
                font-weight: bold;
                font-family: 'Consolas', 'Courier New', monospace;
            """)  # Green
        else:
            self.value_label.setStyleSheet(f"""
                color: #ff6b6b;
                font-size: {self.VALUE_FONT_SIZE}pt;
                font-weight: bold;
                font-family: 'Consolas', 'Courier New', monospace;
            """)  # Red

    def get_value(self) -> float:
        """Get current displayed value."""
        return self._value

    def get_measurement_type(self) -> str:
        """
        Get the currently selected measurement type.

        Returns:
            Measurement type string (e.g., "VOLT:DC").
        """
        return self.measurement_combo.currentData()

    def get_range(self) -> str:
        """
        Get currently selected range.

        Returns:
            Range value string (e.g., "200 mV", "AUTO").
        """
        return self.range_combo.currentData()

    def set_range(self, range_value: str) -> None:
        """
        Set measurement range.

        Args:
            range_value: Range value string (e.g., "200 mV", "AUTO").
        """
        index = self.range_combo.findData(range_value)
        if index >= 0:
            self.range_combo.setCurrentIndex(index)
            # Update unit label based on new range and measurement type
            measurement_type = self.measurement_combo.currentData()
            self._update_unit_for_measurement_type(measurement_type)

    def set_measurement_type(self, measurement_type: str) -> None:
        """
        Set the measurement type.

        Args:
            measurement_type: Measurement type string (e.g., "VOLT:DC").
        """
        index = self.measurement_combo.findData(measurement_type)
        if index >= 0:
            self.measurement_combo.setCurrentIndex(index)
            # Update unit label based on measurement type
            self._update_unit_for_measurement_type(measurement_type)
            # Update range dropdown options for this measurement type
            self._update_range_options(measurement_type)

    def _update_range_options(self, measurement_type: str) -> None:
        """
        Update range dropdown options based on the selected measurement type.

        Args:
            measurement_type: Measurement type string.
        """
        # Save current range value if it's still valid
        current_range = self.range_combo.currentData()
        
        # Clear and repopulate range dropdown
        self.range_combo.clear()
        valid_ranges = self.VALID_RANGES.get(measurement_type, ["AUTO"])
        for range_val in valid_ranges:
            self.range_combo.addItem(range_val, range_val)
        
        # Try to restore previous range value if it's still valid
        if current_range in valid_ranges:
            index = self.range_combo.findData(current_range)
            if index >= 0:
                self.range_combo.setCurrentIndex(index)
        else:
            # Default to AUTO
            index = self.range_combo.findData("AUTO")
            if index >= 0:
                self.range_combo.setCurrentIndex(index)

    def _update_unit_for_measurement_type(self, measurement_type: str) -> None:
        """
        Update the unit label based on the measurement type.

        Args:
            measurement_type: Measurement type string (e.g., "VOLT:DC").
        """
        # Get unit based on current range
        range_value = self.range_combo.currentData()
        if range_value and range_value != "AUTO":
            unit = self.RANGE_TO_UNIT.get(range_value, self.MEASUREMENT_TYPE_TO_UNIT.get(measurement_type, "V"))
        else:
            unit = self.MEASUREMENT_TYPE_TO_UNIT.get(measurement_type, "V")
        self.set_unit(unit)

    def _on_measurement_type_changed(self, index: int) -> None:
        """Handle measurement type combo box change."""
        measurement_type = self.measurement_combo.currentData()
        # Update unit label based on new measurement type
        self._update_unit_for_measurement_type(measurement_type)
        # Update range dropdown options for this measurement type
        self._update_range_options(measurement_type)
        self.measurement_type_changed.emit(self._channel_num, measurement_type)

    def _on_range_changed(self, index: int) -> None:
        """Handle range combo box change."""
        range_value = self.range_combo.currentData()
        measurement_type = self.measurement_combo.currentData()
        
        # Update unit label based on new range and measurement type
        self._update_unit_for_measurement_type(measurement_type)
        
        # Emit signal for range change
        self.range_changed.emit(self._channel_num, range_value)
