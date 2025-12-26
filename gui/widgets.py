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

    measurement_type_changed = Signal(int, str)  # Signal emitted when measurement type changes (channel_num, type)

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
        self._unit = "V"
        self._is_current_channel = channel_num > 12

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

        # Value label (large, readable)
        self.value_label = QLabel("0.0000")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_font = QFont()
        value_font.setPointSize(28)
        value_font.setBold(True)
        value_font.setFamily("Consolas, Courier New, monospace")
        self.value_label.setFont(value_font)
        layout.addWidget(self.value_label)

        # Unit label
        self.unit_label = QLabel(self._unit)
        self.unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        unit_font = QFont()
        unit_font.setPointSize(12)
        unit_font.setBold(True)
        self.unit_label.setFont(unit_font)
        layout.addWidget(self.unit_label)

        # Measurement type selector
        if self._is_current_channel:
            # Current channels (13-16): only AC/DC selection
            self.measurement_combo = QComboBox()
            self.measurement_combo.addItem("DC Current", "CURR:DC")
            self.measurement_combo.addItem("AC Current", "CURR:AC")
            self.measurement_combo.currentIndexChanged.connect(self._on_measurement_type_changed)
            layout.addWidget(self.measurement_combo)
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
            layout.addWidget(self.measurement_combo)

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
        Update the displayed value.

        Args:
            value: New measurement value.
            unit: Unit string to display (optional, uses current unit if not provided).
        """
        self._value = value
        if unit is not None:
            self._unit = unit
            self.unit_label.setText(unit)
        self.value_label.setText(f"{value:.6f}")

    def set_unit(self, unit: str) -> None:
        """
        Update the unit label.

        Args:
            unit: Unit string to display.
        """
        self._unit = unit
        self.unit_label.setText(unit)

    def set_status(self, status: str, error: bool = False) -> None:
        """
        Update the channel status (displayed in value label).

        Args:
            status: Status text to display.
            error: If True, display status in red color.
        """
        self.value_label.setText(status)
        if error:
            self.value_label.setStyleSheet("color: #ff6b6b;")
        else:
            self.value_label.setStyleSheet("color: #51cf66;")

    def reset_status(self) -> None:
        """Reset the value label to normal display."""
        self.value_label.setText(f"{self._value:.6f}")
        self.value_label.setStyleSheet("")

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

    def set_measurement_type(self, measurement_type: str) -> None:
        """
        Set the measurement type.

        Args:
            measurement_type: Measurement type string (e.g., "VOLT:DC").
        """
        index = self.measurement_combo.findData(measurement_type)
        if index >= 0:
            self.measurement_combo.setCurrentIndex(index)

    def _on_measurement_type_changed(self, index: int) -> None:
        """Handle measurement type combo box change."""
        measurement_type = self.measurement_combo.currentData()
        self.measurement_type_changed.emit(self._channel_num, measurement_type)
