"""
Main application window for SDM4055A-SC multimeter controller.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
import logging

from .widgets import DigitalIndicator
from hardware import VisaInterface, VisaSimulator

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window for the multimeter controller application."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        self._device = None  # Will be VisaInterface or VisaSimulator
        self._use_simulator = True  # Set to False to use real device

        # Timer for periodic polling (500ms)
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self._on_poll_timer)

        self._setup_ui()
        self._initialize_device()

    def _setup_ui(self) -> None:
        """Setup the main window UI."""
        self.setWindowTitle("SDM4055A-SC Multimeter Controller")
        self.setMinimumSize(600, 400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Control panel
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel)

        # Measurement display
        self.indicator = DigitalIndicator(title="DC Voltage", unit="V")
        main_layout.addWidget(self.indicator)

        # Add stretch to push content up
        main_layout.addStretch()

    def _create_header(self) -> QFrame:
        """Create application header."""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 10, 15, 10)

        title = QLabel("SDM4055A-SC Controller")
        title.setStyleSheet("color: #ffffff;")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)

        layout.addWidget(title)
        layout.addStretch()

        return header

    def _create_control_panel(self) -> QFrame:
        """Create control panel with connection button."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        layout = QHBoxLayout(panel)
        layout.setContentsMargins(15, 10, 15, 10)

        # Connection button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setFixedWidth(120)
        self.connect_button.clicked.connect(self._toggle_connection)
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5aaaff;
            }
            QPushButton:pressed {
                background-color: #3a8eef;
            }
        """)

        # Status label
        self.status_label = QLabel("Disconnected")
        self.status_label.setStyleSheet("color: #ff6b6b;")
        status_font = QFont()
        status_font.setPointSize(11)
        self.status_label.setFont(status_font)

        layout.addWidget(self.connect_button)
        layout.addWidget(self.status_label)
        layout.addStretch()

        return panel

    def _initialize_device(self) -> None:
        """Initialize device interface (real or simulator)."""
        if self._use_simulator:
            self._device = VisaSimulator()
            logger.info("Initialized simulator mode")
        else:
            self._device = VisaInterface()
            logger.info("Initialized real device mode")

    def _toggle_connection(self) -> None:
        """Toggle device connection."""
        if self._device.is_connected():
            self._disconnect()
        else:
            self._connect()

    def _connect(self) -> None:
        """Connect to the device."""
        if self._device.connect():
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff6b6b;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff7b7b;
                }
                QPushButton:pressed {
                    background-color: #ef5b5b;
                }
            """)
            self.status_label.setText("Connected")
            self.status_label.setStyleSheet("color: #51cf66;")
            self.indicator.set_status("Connected", error=False)

            # Set measurement function
            self._device.set_measurement_function("VOLT:DC")

            # Start polling
            self.poll_timer.start(500)  # 500ms polling interval
            logger.info("Connected and started polling")
        else:
            self.status_label.setText("Connection Failed")
            self.status_label.setStyleSheet("color: #ff6b6b;")
            self.indicator.set_status("Connection Failed", error=True)
            logger.error("Failed to connect to device")

    def _disconnect(self) -> None:
        """Disconnect from the device."""
        self.poll_timer.stop()
        self._device.disconnect()

        self.connect_button.setText("Connect")
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5aaaff;
            }
            QPushButton:pressed {
                background-color: #3a8eef;
            }
        """)
        self.status_label.setText("Disconnected")
        self.status_label.setStyleSheet("color: #ff6b6b;")
        self.indicator.set_status("Disconnected", error=False)
        logger.info("Disconnected and stopped polling")

    def _on_poll_timer(self) -> None:
        """Handle periodic polling timer."""
        value = self._device.read_measurement()

        if value is not None:
            self.indicator.set_value(value, unit="V")
            self.indicator.set_status("Reading", error=False)
        else:
            self.indicator.set_status("Read Error", error=True)
            logger.warning("Failed to read measurement")

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Stop polling and disconnect
        if self.poll_timer.isActive():
            self.poll_timer.stop()
        if self._device and self._device.is_connected():
            self._device.disconnect()
        event.accept()
