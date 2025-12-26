"""
Main application window for SDM4055A-SC multimeter controller with multi-channel scanning support.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QSlider, QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
import logging

from .widgets import DigitalIndicator, ChannelIndicator
from hardware import VisaInterface, VisaSimulator, MeasurementType

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window for the multimeter controller application with multi-channel scanning."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        self._device = None  # Will be VisaInterface or VisaSimulator
        self._use_simulator = False  # Set to False to use real device

        # Timer for multi-channel scanning (default 1s)
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self._on_scan_timer)

        # Channel indicators (1-16)
        self._channel_indicators = {}
        self._scanning = False

        self._setup_ui()
        self._initialize_device()

    def _setup_ui(self) -> None:
        """Setup the main window UI."""
        self.setWindowTitle("SDM4055A-SC Multi-Channel Controller")
        self.setMinimumSize(1200, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header with device address
        header = self._create_header()
        main_layout.addWidget(header)

        # Control panel
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel)

        # Channel grid (scrollable)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        scroll_widget = QWidget()
        self._channel_grid = QGridLayout(scroll_widget)
        self._channel_grid.setSpacing(15)
        
        # Create 16 channel indicators in a 4x4 grid
        for i in range(1, 17):
            indicator = ChannelIndicator(i)
            indicator.measurement_type_changed.connect(self._on_measurement_type_changed)
            self._channel_indicators[i] = indicator
            
            # Calculate grid position (4 columns)
            row = (i - 1) // 4
            col = (i - 1) % 4
            self._channel_grid.addWidget(indicator, row, col)
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

    def _create_header(self) -> QFrame:
        """Create application header with device address."""
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

        title = QLabel("SDM4055A-SC Multi-Channel Controller")
        title.setStyleSheet("color: #ffffff;")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)

        layout.addWidget(title)
        layout.addStretch()

        # Device address label
        self.device_address_label = QLabel("Device: Not connected")
        self.device_address_label.setStyleSheet("color: #aaaaaa;")
        address_font = QFont()
        address_font.setPointSize(11)
        self.device_address_label.setFont(address_font)
        layout.addWidget(self.device_address_label)

        return header

    def _create_control_panel(self) -> QFrame:
        """Create control panel with connection, scanning controls, and interval slider."""
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
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
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
        layout.addSpacing(30)

        # START button
        self.start_button = QPushButton("START")
        self.start_button.setFixedWidth(100)
        self.start_button.clicked.connect(self._start_scanning)
        self.start_button.setEnabled(False)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #51cf66;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #61df76;
            }
            QPushButton:pressed {
                background-color: #41bf56;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)

        # STOP button
        self.stop_button = QPushButton("STOP")
        self.stop_button.setFixedWidth(100)
        self.stop_button.clicked.connect(self._stop_scanning)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addSpacing(30)

        # Scan interval label
        interval_label = QLabel("Scan Interval:")
        interval_label.setStyleSheet("color: #ffffff;")
        interval_font = QFont()
        interval_font.setPointSize(11)
        interval_label.setFont(interval_font)
        layout.addWidget(interval_label)

        # Scan interval slider (4000ms to 10000ms, default 5000ms)
        # Minimum 4s because each channel takes ~200ms (100ms switch + 50ms config + 50ms read)
        # 16 channels * 200ms = 3200ms minimum, plus overhead
        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setMinimum(4000)
        self.interval_slider.setMaximum(10000)
        self.interval_slider.setValue(5000)
        self.interval_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.interval_slider.setTickInterval(1000)
        self.interval_slider.setFixedWidth(200)
        self.interval_slider.valueChanged.connect(self._on_interval_changed)
        self.interval_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #3d3d3d;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4a9eff;
                border: none;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #5aaaff;
            }
        """)
        layout.addWidget(self.interval_slider)

        # Interval value label
        self.interval_value_label = QLabel("5000 ms")
        self.interval_value_label.setStyleSheet("color: #ffffff;")
        self.interval_value_label.setFixedWidth(60)
        interval_value_font = QFont()
        interval_value_font.setPointSize(11)
        interval_value_font.setBold(True)
        self.interval_value_label.setFont(interval_value_font)
        layout.addWidget(self.interval_value_label)

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
            
            # Enable START button
            self.start_button.setEnabled(True)
            
            # Update device address
            device_address = self._device.get_device_address()
            self.device_address_label.setText(f"Device: {device_address}")
            
            # Reset all channel indicators
            for indicator in self._channel_indicators.values():
                indicator.reset_status()
            
            logger.info("Connected successfully")
        else:
            self.status_label.setText("Connection Failed")
            self.status_label.setStyleSheet("color: #ff6b6b;")
            logger.error("Failed to connect to device")

    def _disconnect(self) -> None:
        """Disconnect from the device."""
        # Stop scanning if active
        if self._scanning:
            self._stop_scanning()
        
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
        
        # Disable START button
        self.start_button.setEnabled(False)
        
        # Update device address
        self.device_address_label.setText("Device: Not connected")
        
        # Reset all channel indicators
        for indicator in self._channel_indicators.values():
            indicator.set_status("Disconnected", error=False)
        
        logger.info("Disconnected")

    def _start_scanning(self) -> None:
        """Start multi-channel scanning."""
        if not self._device.is_connected():
            logger.warning("Cannot start scanning: device not connected")
            return
        
        self._scanning = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # Start timer with current interval
        interval = self.interval_slider.value()
        self.scan_timer.start(interval)
        
        logger.info(f"Started scanning with interval {interval}ms")

    def _stop_scanning(self) -> None:
        """Stop multi-channel scanning."""
        self._scanning = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # Stop timer
        self.scan_timer.stop()
        
        logger.info("Stopped scanning")

    def _on_interval_changed(self, value: int) -> None:
        """Handle scan interval slider change."""
        self.interval_value_label.setText(f"{value} ms")
        
        # Update timer interval if scanning
        if self._scanning:
            self.scan_timer.setInterval(value)
            logger.info(f"Updated scan interval to {value}ms")

    def _on_measurement_type_changed(self, channel_num: int, measurement_type: str) -> None:
        """Handle measurement type change for a channel."""
        if self._device and self._device.is_connected():
            # Convert string to MeasurementType enum
            try:
                mt = MeasurementType(measurement_type)
                self._device.set_channel_measurement_type(channel_num, mt)
                logger.info(f"Channel {channel_num} measurement type changed to {measurement_type}")
            except ValueError:
                logger.error(f"Invalid measurement type: {measurement_type}")

    def _on_scan_timer(self) -> None:
        """Handle periodic scanning timer."""
        if not self._device.is_connected():
            self._stop_scanning()
            return
        
        # Read all channels
        measurements = self._device.read_all_channels()
        
        # Update channel indicators
        for channel_num, value in measurements.items():
            indicator = self._channel_indicators.get(channel_num)
            if indicator:
                if value is not None:
                    # Determine unit based on measurement type
                    measurement_type_str = indicator.get_measurement_type()
                    unit = self._get_unit_for_measurement_type(measurement_type_str)
                    indicator.set_value(value, unit)
                    indicator.reset_status()
                else:
                    indicator.set_status("Error", error=True)

    def _get_unit_for_measurement_type(self, measurement_type: str) -> str:
        """
        Get the unit string for a given measurement type.

        Args:
            measurement_type: Measurement type string (e.g., "VOLT:DC").

        Returns:
            Unit string (e.g., "V").
        """
        unit_map = {
            "VOLT:DC": "V",
            "VOLT:AC": "V",
            "CURR:DC": "A",
            "CURR:AC": "A",
            "RES": "Ω",
            "FRES": "Ω",
            "CAP": "F",
            "FREQ": "Hz",
            "DIOD": "V",
            "CONT": "Ω",
            "TEMP:RTD": "°C",
            "TEMP:THER": "°C",
        }
        return unit_map.get(measurement_type, "")

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Stop scanning and disconnect
        if self._scanning:
            self._stop_scanning()
        if self._device and self._device.is_connected():
            self._device.disconnect()
        event.accept()
