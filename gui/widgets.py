"""
Custom GUI widgets for SDM4055A-SC multimeter controller.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPalette, QColor


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
