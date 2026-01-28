"""
Main application window for SDM4055A-SC multimeter controller.
"""
import csv
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import QObject, Signal, Slot, Qt
from PySide6.QtGui import QAction, QMouseEvent, QIcon, QPainter, QPainterPath, QColor, QFontMetrics
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QComboBox,
    QGroupBox,
    QGridLayout,
    QFileDialog,
    QLineEdit,
    QCheckBox,
)

from PySide6.QtWidgets import QStyle

from hardware.visa_interface import VisaInterface, MeasurementType, ScanDataResult
from hardware.async_worker import AsyncScanManager
from hardware.simulator import VisaSimulator
from gui.widgets import ChannelIndicator, LogViewerDialog, QLogHandler, ChannelProgressIndicator
from gui.theme_manager import ThemeManager
from config import ConfigLoader, ChannelThresholdConfig

logger = logging.getLogger(__name__)


class ClickToClearLineEdit(QLineEdit):
    """Custom QLineEdit that clears text when clicked."""

    def __init__(self, parent=None):
        """Initialize the custom line edit.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self._cleared_on_click = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press event to clear text on click.

        Args:
            event: Mouse event.
        """
        # Clear text on first click if not already cleared
        if not self._cleared_on_click and event.button() == Qt.LeftButton:
            self.clear()
            self._cleared_on_click = True
            logger.debug("Serial number field cleared on click")

        # Call parent implementation
        super().mousePressEvent(event)

    def focusOutEvent(self, event) -> None:
        """Handle focus out event to reset cleared state.

        Args:
            event: Focus event.
        """
        self._cleared_on_click = False
        super().focusOutEvent(event)


class MainWindow(QMainWindow):
    """Main application window."""

    # Signals for thread-safe UI updates
    status_updated = Signal(str)
    connection_changed = Signal(bool)
    scan_started = Signal()
    scan_complete = Signal(object)

    def __init__(self, version: str = "1.0.0", theme_manager: Optional[ThemeManager] = None, parent: Optional[QObject] = None) -> None:
        """Initialize main window.

        Args:
            version: Application version string.
            theme_manager: ThemeManager instance for theme switching.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle(f"SDM4055A-SC Multimeter Controller v{version}")
        self.resize(1200, 800)

        # Theme manager
        self._theme_manager = theme_manager
        self._current_theme = "dark"  # Default theme

        # Initialize VISA interface
        self.visa = VisaInterface()

        # Initialize simulator (for testing without hardware)
        self.simulator = VisaSimulator()

        # Flag to track if using simulator
        self._using_simulator = False

        # Async scan manager
        self.scan_manager: Optional[AsyncScanManager] = None

        # Channel indicators (1-16)
        self.channel_indicators: List[ChannelIndicator] = []

        # Channel measurement type configurations (1-16)
        self._channel_measurement_types: Dict[int, str] = {}
        
        # Channel range configurations (1-16)
        self._channel_ranges: Dict[int, str] = {}

        # Configuration loader
        self.config_loader = ConfigLoader()

        # Report file path for saving measurements
        self._report_file_path: Optional[str] = None

        # Log viewer dialog
        self._log_viewer_dialog: Optional[LogViewerDialog] = None

        # Setup Qt log handler for GUI log display
        self._log_handler = QLogHandler(self)
        self._log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        # Add handler to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(self._log_handler)

        # Setup UI
        self._setup_ui()
        self._setup_connections()

        # Initialize default channel measurement types
        self._initialize_channel_measurement_types()

        # Apply initial theme
        if self._theme_manager:
            self._apply_theme(self._theme_manager.get_current_theme())

        # Initial status
        self.status_updated.emit("Ready")

    def _setup_ui(self) -> None:
        """Setup user interface."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Connection control group
        conn_group = QGroupBox("Device Connection")
        conn_layout = QHBoxLayout()

        self.btn_connect = QPushButton("Connect")
        self.btn_connect.clicked.connect(self._on_connect_clicked)

        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_disconnect.clicked.connect(self._on_disconnect_clicked)
        self.btn_disconnect.setEnabled(False)

        self.btn_refresh_devices = QPushButton("Refresh")
        self.btn_refresh_devices.clicked.connect(self._on_refresh_devices)

        self.device_combo = QComboBox()
        # Minimum width to show full device names
        self.device_combo.setMinimumWidth(400)
        self.device_combo.setMinimumContentsLength(
            50)  # Minimum characters to display
        self.device_combo.currentIndexChanged.connect(self._on_device_selected)

        self.device_info_label = QLabel("No device connected")

        self.status_label = QLabel("Disconnected")
        self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")

        conn_layout.addWidget(self.btn_connect)
        conn_layout.addWidget(self.btn_disconnect)
        conn_layout.addWidget(self.btn_refresh_devices)
        conn_layout.addWidget(self.device_combo)
        conn_layout.addWidget(self.device_info_label)
        conn_layout.addWidget(self.status_label)
        conn_layout.addStretch()

        conn_group.setLayout(conn_layout)
        main_layout.addWidget(conn_group)

        # Scan control group
        scan_group = QGroupBox("Scan Control")
        scan_layout = QHBoxLayout()

        # Serial number input section
        self.lbl_serial_number = QLabel("Serial Number:")
        self.serial_number_input = ClickToClearLineEdit()
        self.serial_number_input.setPlaceholderText("PSN123456789")
        # Calculate width based on font metrics for 12 characters (PSN + 9 digits)
        font_metrics = QFontMetrics(self.serial_number_input.font())
        text_width = font_metrics.horizontalAdvance("PSN123456789")
        # Add padding for text margins and border
        self.serial_number_input.setMinimumWidth(text_width + 20)
        self.serial_number_input.textChanged.connect(self._on_serial_number_changed)
        
        scan_layout.addWidget(self.lbl_serial_number)
        scan_layout.addWidget(self.serial_number_input)
        scan_layout.addSpacing(20)

        self.btn_single_scan = QPushButton("Single Scan")
        self.btn_single_scan.clicked.connect(self._single_scan)
        self.btn_single_scan.setEnabled(False)

        self.btn_start_scan = QPushButton("Start Scan")
        self.btn_start_scan.clicked.connect(self._start_scanning)
        self.btn_start_scan.setEnabled(False)
        self.btn_start_scan.setVisible(False)

        self.btn_stop_scan = QPushButton("Stop Scan")
        self.btn_stop_scan.clicked.connect(self._stop_scanning)
        self.btn_stop_scan.setEnabled(False)
        self.btn_stop_scan.setVisible(False)

        # Channel progress indicator instead of text label
        self.scan_progress = ChannelProgressIndicator()

        scan_layout.addWidget(self.btn_single_scan)
        scan_layout.addWidget(self.btn_start_scan)
        scan_layout.addWidget(self.btn_stop_scan)
        scan_layout.addWidget(self.scan_progress)
        
        # Configuration file section
        scan_layout.addSpacing(20)
        self.btn_load_config = QPushButton("Load Config")
        self.btn_load_config.clicked.connect(self._on_load_config_clicked)
        self.lbl_config_file = QLabel("No config loaded")
        self.lbl_config_file.setStyleSheet("color: #888; font-style: italic;")
        
        scan_layout.addWidget(self.btn_load_config)
        scan_layout.addWidget(self.lbl_config_file)
        scan_layout.addSpacing(20)

        # Report file section
        self.btn_select_report_file = QPushButton("Select Report File")
        self.btn_select_report_file.clicked.connect(self._on_select_report_file)
        self.btn_new_report_file = QPushButton("New Report File")
        self.btn_new_report_file.clicked.connect(self._on_new_report_file)
        self.lbl_report_file = QLabel("No report file selected")
        self.lbl_report_file.setStyleSheet("color: #888; font-style: italic;")

        scan_layout.addWidget(self.btn_select_report_file)
        scan_layout.addWidget(self.btn_new_report_file)
        scan_layout.addWidget(self.lbl_report_file)
        scan_layout.addStretch()

        scan_group.setLayout(scan_layout)
        main_layout.addWidget(scan_group)

        # Channel indicators grid (4x4 for 16 channels)
        channels_group = QGroupBox("Channel Measurements")
        channels_layout = QGridLayout()

        self.channel_indicators = []
        for i in range(16):
            row = i // 4
            col = i % 4
            indicator = ChannelIndicator(channel_num=i + 1)
            channels_layout.addWidget(indicator, row, col)
            self.channel_indicators.append(indicator)

        channels_group.setLayout(channels_layout)
        main_layout.addWidget(channels_group)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Add theme toggle button to status bar (left side, before log viewer)
        self.btn_theme_toggle = QPushButton()
        self.btn_theme_toggle.setFixedSize(30, 30)
        self.btn_theme_toggle.clicked.connect(self._toggle_theme)
        self.status_bar.addPermanentWidget(self.btn_theme_toggle, 0)

        # Add log viewer button to status bar (left side)
        self.btn_log_viewer = QPushButton()
        # Use standard icon for terminal/console
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        self.btn_log_viewer.setIcon(icon)
        self.btn_log_viewer.setToolTip("Open Log Viewer")
        self.btn_log_viewer.setFixedSize(30, 30)
        self.btn_log_viewer.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #5d5d5d;
            }
        """)
        self.btn_log_viewer.clicked.connect(self._toggle_log_viewer)
        self.status_bar.addPermanentWidget(self.btn_log_viewer, 0)

        # Update theme button icons and styles after all buttons are created
        self._update_theme_button_icon()

    def _create_yin_yang_icon(self) -> QIcon:
        """
        Create a Yin-Yang symbol icon for theme switching.
        The Yin-Yang symbol represents balance between dark and light.
        
        Returns:
            QIcon containing the Yin-Yang symbol.
        """
        from PySide6.QtGui import QPixmap, QImage
        
        # Create a 64x64 pixmap
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        # Create painter
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Center coordinates
        center_x = size // 2
        center_y = size // 2
        radius = size // 2 - 2  # Leave some margin
        
        # Draw outer circle
        painter.setPen(QColor("#000000"))
        painter.setBrush(QColor("#000000"))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # Draw white half (right side)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#ffffff"))
        painter.drawPie(center_x - radius, center_y - radius, radius * 2, radius * 2, 90 * 16, 180 * 16)
        
        # Draw small white circle on left side
        small_radius = radius // 2
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(center_x - small_radius, center_y - radius, small_radius * 2, small_radius * 2)
        
        # Draw small black circle on right side
        painter.setBrush(QColor("#000000"))
        painter.drawEllipse(center_x - small_radius, center_y, small_radius * 2, small_radius * 2)
        
        # Draw small black dot in white circle (left)
        dot_radius = radius // 6
        painter.setBrush(QColor("#000000"))
        painter.drawEllipse(center_x - dot_radius, center_y - radius // 2 - dot_radius, dot_radius * 2, dot_radius * 2)
        
        # Draw small white dot in black circle (right)
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(center_x - dot_radius, center_y + radius // 2 - dot_radius, dot_radius * 2, dot_radius * 2)
        
        # End painting
        painter.end()
        
        # Create icon from pixmap
        return QIcon(pixmap)

    def _apply_theme(self, theme: str) -> None:
        """
        Apply theme to all UI elements in the main window.

        Args:
            theme: Theme string ("dark" or "light").
        """
        self._current_theme = theme

        if theme == "dark":
            # Dark theme styles
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QGroupBox {
                    color: #ffffff;
                    border: 1px solid #3d3d3d;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                    padding-left: 10px;
                    padding-right: 10px;
                    font-weight: bold;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 10px;
                    background-color: #2d2d2d;
                    color: #cccccc;
                }
                QLabel {
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #4d4d4d;
                    color: #ffffff;
                    border: 1px solid #5d5d5d;
                    border-radius: 4px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #5d5d5d;
                }
                QPushButton:pressed {
                    background-color: #6d6d6d;
                }
                QPushButton:disabled {
                    background-color: #3d3d3d;
                    color: #888888;
                }
                QComboBox {
                    background-color: #4d4d4d;
                    color: #ffffff;
                    border: 1px solid #5d5d5d;
                    border-radius: 4px;
                    padding: 5px;
                }
                QComboBox:hover {
                    background-color: #5d5d5d;
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
                    background-color: #4d4d4d;
                    color: #ffffff;
                    selection-background-color: #4a9eff;
                    border: 1px solid #5d5d5d;
                }
                QLineEdit {
                    background-color: #4d4d4d;
                    color: #ffffff;
                    border: 1px solid #5d5d5d;
                    border-radius: 4px;
                    padding: 5px;
                }
                QLineEdit:focus {
                    border: 1px solid #4a9eff;
                }
            """)
        else:
            # Light theme styles
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                    color: #000000;
                }
                QGroupBox {
                    color: #000000;
                    border: 1px solid #d0d0d0;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                    padding-left: 10px;
                    padding-right: 10px;
                    font-weight: bold;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 10px;
                    background-color: #f5f5f5;
                    color: #666666;
                }
                QLabel {
                    color: #000000;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: #000000;
                    border: 1px solid #b0b0b0;
                    border-radius: 4px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QPushButton:disabled {
                    background-color: #e8e8e8;
                    color: #666666;
                }
                QComboBox {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #b0b0b0;
                    border-radius: 4px;
                    padding: 5px;
                }
                QComboBox:hover {
                    background-color: #f0f0f0;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 5px solid #000000;
                    margin-right: 5px;
                }
                QComboBox QAbstractItemView {
                    background-color: #ffffff;
                    color: #000000;
                    selection-background-color: #4a9eff;
                    border: 1px solid #b0b0b0;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #b0b0b0;
                    border-radius: 4px;
                    padding: 5px;
                }
                QLineEdit:focus {
                    border: 1px solid #4a9eff;
                }
            """)

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self.status_updated.connect(self.status_bar.showMessage)
        self.connection_changed.connect(self._on_connection_changed)
        self.scan_started.connect(self._on_scan_started)
        self.scan_complete.connect(self._on_scan_complete)

        # Connect theme manager signal
        if self._theme_manager:
            self._theme_manager.theme_changed.connect(self._on_theme_changed)

        # Connect channel measurement type change signals
        for indicator in self.channel_indicators:
            indicator.measurement_type_changed.connect(
                self._on_channel_measurement_type_changed)
            # Connect channel range change signals
            indicator.range_changed.connect(
                self._on_channel_range_changed)

    @Slot()
    def _on_connect_clicked(self) -> None:
        """Handle connect button click."""
        self.status_updated.emit("Connecting to device...")
        QApplication.processEvents()

        # Get selected device from combo box
        selected_device = self.device_combo.currentData()

        # Check if simulator is selected
        if selected_device == "SIMULATOR":
            self._using_simulator = True
            logger.info("Using simulator mode")

            # Connect to simulator
            success = self.simulator.connect()

            if success:
                # Update device info display
                device_info = self.simulator.get_device_info()
                self._update_device_info_display(device_info)

                self.status_label.setText("Connected (Simulator)")
                self.status_label.setStyleSheet(
                    "color: #51cf66; font-weight: bold;")
                self.btn_connect.setEnabled(False)
                self.btn_disconnect.setEnabled(True)
                self.btn_start_scan.setEnabled(True)
                self.btn_single_scan.setEnabled(True)
                self.connection_changed.emit(True)
                self.status_updated.emit("Connected to Simulator")
                logger.info("Successfully connected to simulator")
            else:
                self.status_label.setText("Error")
                self.status_label.setStyleSheet(
                    "color: #ff6b6b; font-weight: bold;")
                QMessageBox.critical(
                    self,
                    "Connection Error",
                    "Failed to connect to simulator.",
                )
                self.status_updated.emit("Connection failed")
                logger.error("Failed to connect to simulator")
        else:
            # Connect to physical device
            self._using_simulator = False
            if selected_device:
                self.visa.resource_string = selected_device
                logger.info(f"Using selected device: {selected_device}")

            # Try to connect
            success = self.visa.connect()

            if success:
                # Update device info display
                device_info = self.visa.get_device_info()
                self._update_device_info_display(device_info)

                self.status_label.setText("Connected")
                self.status_label.setStyleSheet(
                    "color: #51cf66; font-weight: bold;")
                self.btn_connect.setEnabled(False)
                self.btn_disconnect.setEnabled(True)
                self.btn_start_scan.setEnabled(True)
                self.btn_single_scan.setEnabled(True)
                self.connection_changed.emit(True)
                self.status_updated.emit("Connected to SDM4055A-SC")
                logger.info("Successfully connected to device")
            else:
                self.status_label.setText("Error")
                self.status_label.setStyleSheet(
                    "color: #ff6b6b; font-weight: bold;")
                QMessageBox.critical(
                    self,
                    "Connection Error",
                    "Failed to connect to device. Please check:\n"
                    "1. Device is powered on\n"
                    "2. USB cable is connected\n"
                    "3. VISA drivers are installed",
                )
                self.status_updated.emit("Connection failed")
                logger.error("Failed to connect to device")

    @Slot()
    def _on_disconnect_clicked(self) -> None:
        """Handle disconnect button click."""
        # Stop scanning if active
        if self.scan_manager is not None and self.scan_manager.is_scanning():
            self._stop_scanning()

        # Disconnect
        if self._using_simulator:
            self.simulator.disconnect()
            logger.info("Disconnected from simulator")
        else:
            self.visa.disconnect()
            logger.info("Disconnected from device")

        # Update UI
        self.status_label.setText("Disconnected")
        self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        self.btn_connect.setEnabled(True)
        self.btn_disconnect.setEnabled(False)
        self.btn_start_scan.setEnabled(False)
        self.btn_single_scan.setEnabled(False)
        self.device_combo.setEnabled(True)
        self.device_info_label.setText("No device connected")
        self.connection_changed.emit(False)
        self.status_updated.emit("Disconnected from device")
        self._using_simulator = False

    def _initialize_channel_measurement_types(self) -> None:
        """Initialize default measurement types and ranges for all channels."""
        for i in range(1, 17):
            if i <= 12:
                # Channels 1-12: default to DC voltage
                self._channel_measurement_types[i] = MeasurementType.VOLTAGE_DC.value
            else:
                # Channels 13-16: default to DC current
                self._channel_measurement_types[i] = MeasurementType.CURRENT_DC.value
            
            # Default all channels to AUTO range
            self._channel_ranges[i] = "AUTO"
        
        # Update unit labels and ranges for all channel indicators based on defaults
        for i, indicator in enumerate(self.channel_indicators, start=1):
            measurement_type = self._channel_measurement_types[i]
            range_value = self._channel_ranges[i]
            indicator.set_measurement_type(measurement_type)
            indicator.set_range(range_value)

    @Slot(int, str)
    def _on_channel_measurement_type_changed(self, channel_num: int, measurement_type: str) -> None:
        """Handle channel measurement type change.

        Args:
            channel_num: Channel number (1-16).
            measurement_type: New measurement type string.
        """
        logger.info(
            f"Channel {channel_num} measurement type changed to {measurement_type}")
        self._channel_measurement_types[channel_num] = measurement_type

    def get_all_channel_measurement_types(self) -> Dict[int, Dict[str, str]]:
        """
        Get measurement types and ranges for all channels.

        Returns:
            Dictionary mapping channel numbers to config dicts with 'measurement_type' and 'range_value'.
        """
        channel_configs = {}
        for i in range(1, 17):
            channel_configs[i] = {
                'measurement_type': self._channel_measurement_types[i],
                'range_value': self._channel_ranges[i]
            }
        return channel_configs

    @Slot(bool)
    def _on_connection_changed(self, connected: bool) -> None:
        """Handle connection state change."""
        if not connected:
            # Reset all channel indicators
            for indicator in self.channel_indicators:
                indicator.reset_status()

    @Slot(str)
    def _on_theme_changed(self, theme: str) -> None:
        """Handle theme change signal.

        Args:
            theme: New theme string ("dark" or "light").
        """
        # Update theme button icon
        self._update_theme_button_icon()

        # Apply theme to main window
        self._apply_theme(theme)

        # Update all channel indicators' themes
        for indicator in self.channel_indicators:
            indicator.update_theme(theme)

        # Update progress indicator theme
        self.scan_progress.update_theme(theme)

        # Update log viewer theme if open
        if self._log_viewer_dialog is not None and self._log_viewer_dialog.isVisible():
            self._log_viewer_dialog.update_theme(theme)

    def _start_scanning(self) -> None:
        """Start continuous scanning."""
        # Check connection status based on mode
        if self._using_simulator:
            if not self.simulator.is_connected():
                QMessageBox.warning(self, "Not Connected",
                                    "Please connect to simulator first")
                return
            device_interface = self.simulator
        else:
            if not self.visa.is_connected():
                QMessageBox.warning(self, "Not Connected",
                                    "Please connect to device first")
                return
            device_interface = self.visa

        # Stop any existing scan
        if self.scan_manager is not None and self.scan_manager.is_scanning():
            self.scan_manager.stop()

        # Create new scan manager
        self.scan_manager = AsyncScanManager(device_interface)

        # Configure device with channel measurement types and ranges
        channel_configs = self.get_all_channel_measurement_types()
        if not self.scan_manager.configure_channels(channel_configs):
            QMessageBox.warning(self, "Configuration Error",
                                "Failed to configure channels with measurement types and ranges")
            return

        # Connect signals
        self.scan_manager.scan_complete.connect(self.scan_complete.emit)
        self.scan_manager.scan_started.connect(self.scan_started.emit)
        self.scan_manager.channel_read.connect(self._on_channel_read)
        self.scan_manager.scan_stopped.connect(self._on_scan_stopped)

        # Start scanning
        self.scan_manager.start()

        logger.info("Started scanning")

    def _stop_scanning(self) -> None:
        """Stop continuous scanning."""
        if self.scan_manager is not None and self.scan_manager.is_scanning():
            self.scan_manager.stop()
            logger.info("Stopped scanning")

    def _single_scan(self) -> None:
        """Perform a single scan of all channels."""
        # Check connection status based on mode
        if self._using_simulator:
            if not self.simulator.is_connected():
                QMessageBox.warning(self, "Not Connected",
                                    "Please connect to simulator first")
                return
            device_interface = self.simulator
        else:
            if not self.visa.is_connected():
                QMessageBox.warning(self, "Not Connected",
                                    "Please connect to device first")
                return
            device_interface = self.visa

        self.status_updated.emit("Performing single scan...")
        self.scan_progress.start_scan()

        # Create temporary scan manager for single scan
        temp_scan_manager = AsyncScanManager(device_interface)

        # Configure device with channel measurement types and ranges
        channel_configs = self.get_all_channel_measurement_types()
        if not temp_scan_manager.configure_channels(channel_configs):
            QMessageBox.warning(self, "Configuration Error",
                                "Failed to configure channels with measurement types and ranges")
            return

        # Connect signals
        temp_scan_manager.scan_complete.connect(self._on_single_scan_complete)
        temp_scan_manager.channel_read.connect(self._on_channel_read)
        temp_scan_manager.scan_started.connect(self._on_single_scan_started)
        temp_scan_manager.scan_error.connect(self._on_single_scan_error)

        # Keep reference to temporary manager to prevent premature garbage collection
        self._temp_scan_manager = temp_scan_manager

        # Perform single scan asynchronously (non-blocking)
        temp_scan_manager.start_single_scan()
        logger.info("Single scan initiated")

    @Slot()
    def _on_scan_started(self) -> None:
        """Handle scan started signal."""
        self.btn_start_scan.setEnabled(False)
        self.btn_stop_scan.setEnabled(True)
        self.btn_single_scan.setEnabled(True)
        self.scan_progress.start_scan()
        self.status_updated.emit("Scanning started")

    @Slot(object)
    def _on_scan_complete(self, measurements) -> None:
        """Handle scan complete signal.

        Args:
            measurements: Dictionary mapping channel numbers to ScanDataResult objects (or None)
        """
        logger.info(f"Scan complete. Measurements: {measurements}")

        # Update all channel indicators with new measurements
        for channel_num, result in measurements.items():
            if 1 <= channel_num <= 16:
                indicator = self.channel_indicators[channel_num - 1]
                
                if result is None:
                    # No data available for this channel
                    indicator.set_status("No data", error=True)
                elif result.unit == "OVERLOAD":
                    # Overload condition detected
                    indicator.set_status(result.full_unit, error=True)
                else:
                    # Valid measurement - update with value and unit
                    indicator.set_value(result.value, result.unit)

        # Update progress indicator
        self.scan_progress.complete_scan()
        self.status_updated.emit(
            f"Scan complete - {len(measurements)} channels measured")

    @Slot()
    def _on_scan_stopped(self) -> None:
        """Handle scan stopped signal."""
        self.btn_start_scan.setEnabled(True)
        self.btn_stop_scan.setEnabled(False)
        self.btn_single_scan.setEnabled(True)
        self.scan_progress.reset()
        self.status_updated.emit("Scanning stopped")
        logger.info("Scan stopped, UI updated")

    @Slot(object)
    def _on_single_scan_complete(self, measurements) -> None:
        """Handle single scan complete signal.

        Args:
            measurements: Dictionary mapping channel numbers to ScanDataResult objects (or None)
        """
        logger.info(f"Single scan complete. Measurements: {measurements}")

        # Clear temporary scan manager reference to allow cleanup
        if hasattr(self, '_temp_scan_manager') and self._temp_scan_manager:
            self._temp_scan_manager = None

        # Re-enable single scan button
        self.btn_single_scan.setEnabled(True)

        # Check if serial number is provided
        serial_number = self.serial_number_input.text().strip()
        if not serial_number:
            QMessageBox.warning(
                self,
                "Missing Serial Number",
                "Please enter a serial number before scanning.\n"
                "The serial number is required for the report."
            )
            self.scan_progress.reset()
            logger.warning("Scan complete but no serial number provided")
            return

        # Validate serial number format
        pattern = r'^PSN\d{9}$'
        if not re.match(pattern, serial_number):
            QMessageBox.warning(
                self,
                "Invalid Serial Number",
                "Please enter a valid serial number in format PSN123456789.\n"
                "The serial number must start with PSN followed by exactly 9 digits."
            )
            self.scan_progress.reset()
            logger.warning(f"Scan complete but invalid serial number format: {serial_number}")
            return

        logger.info(f"Serial number validated: {serial_number}")

        # Update all channel indicators with new measurements
        for channel_num, result in measurements.items():
            if 1 <= channel_num <= 16:
                indicator = self.channel_indicators[channel_num - 1]

                if result is None:
                    # No data available for this channel
                    indicator.set_status("No data", error=True)
                elif result.unit == "OVERLOAD":
                    # Overload condition detected
                    indicator.set_status(result.full_unit, error=True)
                else:
                    # Valid measurement - update with value and unit
                    indicator.set_value(result.value, result.unit)

        # Write to report file
        logger.info("Writing measurements to report file...")
        self._write_report_row(serial_number, measurements)

        # Check if serial number exists in report and update color
        logger.info("Checking serial number in report after write...")
        if self._check_serial_in_report(serial_number):
            self.serial_number_input.setStyleSheet("color: #51cf66; font-weight: bold;")
            logger.info(f"Serial number '{serial_number}' confirmed in report, set green color")
        else:
            self.serial_number_input.setStyleSheet("color: white;")
            logger.info(f"Serial number '{serial_number}' not found in report, set white color")

        # Update progress indicator
        self.scan_progress.complete_scan()
        self.status_updated.emit("Ready")

    @Slot()
    def _on_single_scan_started(self) -> None:
        """Handle single scan started signal."""
        self.btn_single_scan.setEnabled(False)
        logger.info("Single scan started")

    @Slot(str)
    def _on_single_scan_error(self, error_msg: str) -> None:
        """Handle single scan error signal.
        
        Args:
            error_msg: Error message string.
        """
        logger.error(f"Single scan error: {error_msg}")
        self.scan_progress.reset()
        self.btn_single_scan.setEnabled(True)
        QMessageBox.critical(
            self,
            "Scan Error",
            f"Failed to perform scan:\n{error_msg}"
        )

    @Slot(int, object)
    def _on_channel_read(self, channel_num: int, result: object) -> None:
        """Handle individual channel read signal.

        Args:
            channel_num: Channel number (1-16)
            result: ScanDataResult object or None
        """
        logger.debug(f"Channel {channel_num} read: {result}")

        # Only update indicator if scan is still running
        # Don't set status here - let _on_scan_complete handle final display
        if 1 <= channel_num <= 16:
            indicator = self.channel_indicators[channel_num - 1]
            
            if result is None:
                # No data available for this channel
                indicator.set_status("No data", error=True)
            elif isinstance(result, ScanDataResult) and result.unit == "OVERLOAD":
                # Overload condition detected
                indicator.set_status(result.full_unit, error=True)
            elif isinstance(result, ScanDataResult):
                # Valid measurement - update with value and unit
                indicator.set_value(result.value, result.unit)
            else:
                # Fallback for backward compatibility (if result is a float)
                indicator.set_value(float(result))

    def _toggle_log_viewer(self) -> None:
        """Toggle log viewer window visibility."""
        if self._log_viewer_dialog is None:
            # Create log viewer dialog
            self._log_viewer_dialog = LogViewerDialog(self, theme_manager=self._theme_manager)
            # Connect log handler to dialog
            if hasattr(self, '_log_handler') and self._log_handler is not None:
                self._log_handler.log_received.connect(self._log_viewer_dialog.add_log)
            self._log_viewer_dialog.show()
        elif self._log_viewer_dialog.isVisible():
            self._log_viewer_dialog.hide()
        else:
            self._log_viewer_dialog.show()
            # Force focus to ensure auto-scroll works
            self._log_viewer_dialog.activateWindow()
            self._log_viewer_dialog.raise_()

    def _toggle_theme(self) -> None:
        """Toggle between dark and light themes."""
        if self._theme_manager:
            self._theme_manager.toggle_theme()
            self._update_theme_button_icon()

    def _update_theme_button_icon(self) -> None:
        """Update theme toggle button icon based on current theme."""
        if self._theme_manager is None:
            return

        current_theme = self._theme_manager.get_current_theme()
        
        # Create and set Yin-Yang icon
        yin_yang_icon = self._create_yin_yang_icon()
        self.btn_theme_toggle.setIcon(yin_yang_icon)
        
        if current_theme == "dark":
            # Dark theme - tooltip indicates switching to light
            self.btn_theme_toggle.setToolTip("Switch to Light Theme")
            self.btn_theme_toggle.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                }
                QPushButton:pressed {
                    background-color: #5d5d5d;
                }
            """)
        else:
            # Light theme - tooltip indicates switching to dark
            self.btn_theme_toggle.setToolTip("Switch to Dark Theme")
            self.btn_theme_toggle.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:pressed {
                    background-color: #b0b0b0;
                }
            """)
        # Update log viewer button style
        if current_theme == "dark":
            self.btn_log_viewer.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                }
                QPushButton:pressed {
                    background-color: #5d5d5d;
                }
            """)
        else:
            self.btn_log_viewer.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:pressed {
                    background-color: #b0b0b0;
                }
            """)

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Stop scanning
        if self.scan_manager is not None and self.scan_manager.is_scanning():
            self.scan_manager.stop()

        # Disconnect from device
        if self._using_simulator:
            if self.simulator.is_connected():
                self.simulator.disconnect()
        else:
            if self.visa.is_connected():
                self.visa.disconnect()

        # Disconnect log handler
        if self._log_handler is not None:
            root_logger = logging.getLogger()
            root_logger.removeHandler(self._log_handler)

        event.accept()
        logger.info("Application closed")

    def _on_refresh_devices(self) -> None:
        """Handle refresh devices button click."""
        self.status_updated.emit("Scanning for devices...")
        QApplication.processEvents()

        # Get available devices
        resources = self.visa.list_available_resources()

        # Update device combo box
        self.device_combo.clear()

        # Add simulator option first
        simulator_name = "SIMULATOR - Virtual SDM4055A-SC (for testing)"
        self.device_combo.addItem(simulator_name, "SIMULATOR")
        logger.debug("Added simulator to device list")

        if resources:
            for resource in resources:
                self.device_combo.addItem(resource, resource)
                logger.debug(f"Added device to list: {resource}")
            self.device_combo.setEnabled(True)

            # Select first device by default (simulator)
            self.device_combo.setCurrentIndex(0)
            logger.info(f"Auto-selected device: SIMULATOR")

            self.status_updated.emit(
                f"Found {len(resources)} device(s) + Simulator")
        else:
            self.device_combo.setEnabled(True)
            self.status_updated.emit(
                "Simulator available (no physical devices found)")
            logger.warning("No VISA resources found, only simulator available")

    def _on_device_selected(self, index: int) -> None:
        """Handle device selection from combo box."""
        if index >= 0:
            selected_device = self.device_combo.currentData()
            logger.info(f"Device selected: {selected_device}")
            self.status_updated.emit(f"Selected: {selected_device}")

    def _update_device_info_display(self, device_info: Dict[str, str]) -> None:
        """Update device information display."""
        if device_info:
            manufacturer = device_info.get('manufacturer', 'Unknown')
            model = device_info.get('model', 'Unknown')
            serial = device_info.get('serial_number', 'Unknown')
            address = device_info.get('address', 'Unknown')

            info_text = f"{manufacturer} | {model} | SN: {serial}"
            self.device_info_label.setText(info_text)
            self.device_info_label.setToolTip(f"Address: {address}")
            logger.info(f"Device info: {device_info}")
        else:
            self.device_info_label.setText("No device connected")
            self.device_info_label.setToolTip("")
    
    def _on_load_config_clicked(self) -> None:
        """Handle load configuration button click."""
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Channel Configuration",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Load configuration
        self.status_updated.emit(f"Loading configuration from {file_path}...")
        QApplication.processEvents()
        
        success, message = self.config_loader.load_from_file(file_path)
        
        if not success:
            QMessageBox.critical(
                self,
                "Configuration Error",
                f"Failed to load configuration:\n{message}"
            )
            self.status_updated.emit("Configuration load failed")
            logger.error(f"Configuration load failed: {message}")
            return
        
        # Apply configuration to channels
        self._apply_configuration()
        
        # Update UI
        config_name = self.config_loader.get_config_file_name()
        self.lbl_config_file.setText(config_name)
        self.lbl_config_file.setStyleSheet("color: #51cf66; font-weight: bold;")
        
        self.status_updated.emit(message)
        logger.info(f"Configuration loaded successfully: {message}")
        
        QMessageBox.information(
            self,
            "Configuration Loaded",
            f"{message}\n\nThresholds have been applied to configured channels.\n"
            "Values within thresholds will display in GREEN.\n"
            "Values outside thresholds will display in RED."
        )
    
    def _apply_configuration(self) -> None:
        """Apply loaded configuration to channel indicators."""
        configs = self.config_loader.get_all_configs()
        
        # Clear all thresholds first
        for indicator in self.channel_indicators:
            indicator.clear_thresholds()
        
        # Apply configuration to each configured channel
        for channel_num, config in configs.items():
            if 1 <= channel_num <= 16:
                indicator = self.channel_indicators[channel_num - 1]
                
                # Set measurement type
                indicator.set_measurement_type(config.measurement_type)
                
                # Update internal measurement type mapping
                self._channel_measurement_types[channel_num] = config.measurement_type
                
                # Set range if specified
                if config.range_value:
                    indicator.set_range(config.range_value)
                    self._channel_ranges[channel_num] = config.range_value
                else:
                    # Default to AUTO if not specified
                    self._channel_ranges[channel_num] = "AUTO"
                
                # Set thresholds
                indicator.set_thresholds(config.lower_threshold, config.upper_threshold)
                
                logger.info(
                    f"Applied config to channel {channel_num}: "
                    f"type={config.measurement_type}, "
                    f"range={config.range_value}, "
                    f"lower={config.lower_threshold}, "
                    f"upper={config.upper_threshold}"
                )
        
        configured_channels = self.config_loader.get_configured_channels()
        logger.info(f"Applied configuration to {len(configured_channels)} channels: {configured_channels}")

    @Slot(int, str)
    def _on_channel_range_changed(self, channel_num: int, range_value: str) -> None:
        """Handle channel range change.

        Args:
            channel_num: Channel number (1-16).
            range_value: New range value string.
        """
        logger.info(
            f"Channel {channel_num} range changed to {range_value}")
        self._channel_ranges[channel_num] = range_value

    def _on_serial_number_changed(self, text: str) -> None:
        """Handle serial number input text change.

        Args:
            text: Current text in the serial number input field.
        """
        # Validate serial number format: PSN followed by exactly 9 digits
        pattern = r'^PSN\d{9}$'

        if text == "":
            # Empty input - use default color
            self.serial_number_input.setStyleSheet("")
        elif re.match(pattern, text):
            # Valid format - check if it exists in report
            if self._check_serial_in_report(text):
                # Serial number exists in report - green color
                self.serial_number_input.setStyleSheet("color: #51cf66; font-weight: bold;")
                logger.debug(f"Valid serial number (exists in report): {text}")
            else:
                # Serial number doesn't exist - white color
                self.serial_number_input.setStyleSheet("color: white;")
                logger.debug(f"Valid serial number (new): {text}")
        else:
            # Invalid format - red color
            self.serial_number_input.setStyleSheet("color: red;")
            logger.debug(f"Invalid serial number: {text}")

    def _on_select_report_file(self) -> None:
        """Handle select report file button click."""
        # Open file dialog to select existing CSV file
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Report File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Store the selected file path
        self._report_file_path = file_path
        
        # Update the label to show the filename
        filename = os.path.basename(file_path)
        self.lbl_report_file.setText(filename)
        self.lbl_report_file.setStyleSheet("color: #51cf66; font-weight: bold;")
        
        self.status_updated.emit(f"Report file selected: {filename}")
        logger.info(f"Report file selected: {file_path}")

    def _on_new_report_file(self) -> None:
        """Handle new report file button click."""
        # Generate filename based on config file and current date
        filename = self._generate_report_filename()
        
        # Open file dialog to save new CSV file
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Create New Report File",
            filename,
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Create empty file
        try:
            with open(file_path, 'w', newline='') as f:
                # Create empty CSV file (content will be added later)
                pass
            
            # Store the file path
            self._report_file_path = file_path
            
            # Update the label to show the filename
            filename = os.path.basename(file_path)
            self.lbl_report_file.setText(filename)
            self.lbl_report_file.setStyleSheet("color: #51cf66; font-weight: bold;")
            
            self.status_updated.emit(f"New report file created: {filename}")
            logger.info(f"New report file created: {file_path}")
        except Exception as e:
            QMessageBox.critical(
                self,
                "File Error",
                f"Failed to create report file:\n{str(e)}"
            )
            logger.error(f"Failed to create report file: {str(e)}")

    def _generate_report_filename(self) -> str:
        """Generate report filename based on config file and current date.
        
        Returns:
            Generated filename in format: <config_name>_<YYYY-MM-DD>.csv or report_<YYYY-MM-DD>.csv
        """
        # Get current date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get config file name if available
        config_name = self.config_loader.get_config_file_name()
        
        if config_name and config_name != "No config loaded":
            # Remove .csv extension from config name
            if config_name.endswith('.csv'):
                config_name = config_name[:-4]
            return f"{config_name}_{current_date}.csv"
        else:
            # No config file loaded, use default name
            return f"report_{current_date}.csv"

    def _check_serial_in_report(self, serial_number: str) -> bool:
        """Check if serial number already exists in report file.

        Args:
            serial_number: Serial number to check

        Returns:
            True if serial number exists in report, False otherwise
        """
        logger.info(f"Checking if serial number '{serial_number}' exists in report file...")

        if not self._report_file_path:
            logger.info("No report file path set")
            return False

        if not os.path.exists(self._report_file_path):
            logger.info(f"Report file does not exist: {self._report_file_path}")
            return False

        try:
            with open(self._report_file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    if row and row[0] == serial_number:
                        logger.info(f"Serial number '{serial_number}' found in report")
                        return True
            logger.info(f"Serial number '{serial_number}' not found in report")
            return False
        except Exception as e:
            logger.error(f"Error checking serial number in report: {e}")
            return False

    def _validate_measurements(self, measurements: Dict[int, Optional[ScanDataResult]]) -> Tuple[bool, str]:
        """Validate measurements against configured thresholds.

        Args:
            measurements: Dictionary of channel measurements

        Returns:
            Tuple of (is_valid, result_string) where:
            - is_valid: True if all measurements are within thresholds
            - result_string: "OK" if valid, "FAILED <details>" if invalid
        """
        logger.info("Validating measurements against thresholds...")

        configs = self.config_loader.get_all_configs()
        failed_channels = []

        for channel_num, result in measurements.items():
            # Only check channels 1-12 (voltage channels)
            if channel_num < 1 or channel_num > 12:
                logger.debug(f"Skipping channel {channel_num} (not in range 1-12)")
                continue

            if result is None:
                logger.debug(f"Channel {channel_num}: No measurement data")
                continue

            if result.unit == "OVERLOAD":
                logger.debug(f"Channel {channel_num}: OVERLOAD condition")
                continue

            config = configs.get(channel_num)
            if config is None:
                logger.debug(f"Channel {channel_num}: No configuration")
                continue

            # Check if thresholds are configured
            if config.lower_threshold is not None and config.upper_threshold is not None:
                if result.value < config.lower_threshold or result.value > config.upper_threshold:
                    # Build channel identifier with custom name if available
                    channel_id = f"CH{channel_num}"
                    if config.name:
                        channel_id = f"CH{channel_num} ({config.name})"
                    failed_channels.append(
                        f"{channel_id}: {result.value:.7f} "
                        f"(expected: {config.lower_threshold} - {config.upper_threshold})"
                    )
                    logger.warning(
                        f"Channel {channel_num} FAILED: value={result.value:.7f}, "
                        f"thresholds=[{config.lower_threshold}, {config.upper_threshold}]"
                    )
                else:
                    logger.debug(f"Channel {channel_num} OK: value={result.value:.7f}")
            elif config.lower_threshold is not None:
                if result.value < config.lower_threshold:
                    # Build channel identifier with custom name if available
                    channel_id = f"CH{channel_num}"
                    if config.name:
                        channel_id = f"CH{channel_num} ({config.name})"
                    failed_channels.append(
                        f"{channel_id}: {result.value:.7f} "
                        f"(expected >= {config.lower_threshold})"
                    )
                    logger.warning(
                        f"Channel {channel_num} FAILED: value={result.value:.7f}, "
                        f"lower_threshold={config.lower_threshold}"
                    )
                else:
                    logger.debug(f"Channel {channel_num} OK: value={result.value:.7f}")
            elif config.upper_threshold is not None:
                if result.value > config.upper_threshold:
                    # Build channel identifier with custom name if available
                    channel_id = f"CH{channel_num}"
                    if config.name:
                        channel_id = f"CH{channel_num} ({config.name})"
                    failed_channels.append(
                        f"{channel_id}: {result.value:.7f} "
                        f"(expected <= {config.upper_threshold})"
                    )
                    logger.warning(
                        f"Channel {channel_num} FAILED: value={result.value:.7f}, "
                        f"upper_threshold={config.upper_threshold}"
                    )
                else:
                    logger.debug(f"Channel {channel_num} OK: value={result.value:.7f}")
            else:
                logger.debug(f"Channel {channel_num}: No thresholds configured")

        if failed_channels:
            result_string = "FAILED " + "; ".join(failed_channels)
            logger.info(f"Validation FAILED: {result_string}")
            return False, result_string
        else:
            logger.info("Validation OK: All measurements within thresholds")
            return True, ""

    def _write_report_row(self, serial_number: str, measurements: Dict[int, Optional[ScanDataResult]]) -> None:
        """Write or update a row in the report file.

        Args:
            serial_number: Serial number from input field
            measurements: Dictionary of channel measurements
        """
        logger.info("=" * 60)
        logger.info("STARTING REPORT FILE WRITE OPERATION")
        logger.info("=" * 60)

        # Check if report file path is set
        if not self._report_file_path:
            logger.warning("No report file selected, skipping report write")
            logger.info("=" * 60)
            return

        logger.info(f"Report file path: {self._report_file_path}")
        logger.info(f"Serial number: {serial_number}")
        logger.info(f"Number of measurements: {len(measurements)}")

        # Validate measurements and get result string
        logger.info("Validating measurements against thresholds...")
        is_valid, result_string = self._validate_measurements(measurements)
        logger.info(f"Validation result: {'OK' if is_valid else 'FAILED'}")
        logger.info(f"Result string: {result_string}")

        # Build row data: [serial_number, result_string]
        row_data = [serial_number, result_string]
        logger.info(f"Building row data. Initial columns: {row_data}")

        # Add voltage measurements for channels 1-12
        configs = self.config_loader.get_all_configs()
        logger.info(f"Loaded {len(configs)} channel configurations")

        for channel_num in range(1, 13):
            result = measurements.get(channel_num)
            config = configs.get(channel_num)

            if result is None or result.unit == "OVERLOAD":
                row_data.append("")
                logger.debug(f"Channel {channel_num}: No data or OVERLOAD, adding empty cell")
            elif config is None:
                row_data.append("")
                logger.debug(f"Channel {channel_num}: No configuration, adding empty cell")
            else:
                row_data.append(f"{result.value:.7f}")
                logger.debug(f"Channel {channel_num}: {result.value:.7f} {result.unit}")

        # Add current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data.append(current_datetime)
        logger.info(f"Date/Time: {current_datetime}")
        logger.info(f"Final row data: {row_data}")
        logger.info(f"Total columns in row: {len(row_data)}")

        # Read existing rows
        rows = []
        file_exists = os.path.exists(self._report_file_path)
        logger.info(f"File exists: {file_exists}")

        if file_exists:
            logger.info("Reading existing file content...")
            try:
                with open(self._report_file_path, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=';')
                    rows = list(reader)
                logger.info(f"Read {len(rows)} rows from file")
                if rows:
                    logger.info(f"First row (header?): {rows[0]}")
            except Exception as e:
                logger.error(f"Error reading report file: {e}")
                logger.exception("Full exception details:")
                rows = []
        else:
            logger.info("File does not exist, will create new file")

        # Check if header exists, add if not
        has_header = False
        if rows:
            has_header = rows[0][0] == "QR"
            logger.info(f"Has valid header: {has_header}")

        if not has_header:
            logger.info("Adding header row...")
            header = ["QR", "TEST RESULT"]
            # Use custom names from channel config if available, otherwise use generic names
            configs = self.config_loader.get_all_configs()
            for i in range(1, 13):
                config = configs.get(i)
                if config and config.name:
                    # Use custom name if configured: "CH1 (custom_name)"
                    header.append(f"CH{i} ({config.name})")
                else:
                    # Use generic name if no custom name: "CH1"
                    header.append(f"CH{i}")
            header.append("Date/Time")
            rows.insert(0, header)
            logger.info(f"Header: {header}")

        # Find and update or append row
        row_found = False
        logger.info(f"Searching for existing row with serial number '{serial_number}'...")
        for i, row in enumerate(rows):
            if row and row[0] == serial_number:
                logger.info(f"Found existing row at index {i}")
                logger.info(f"Old row: {row}")
                rows[i] = row_data
                row_found = True
                logger.info(f"Updated row: {row_data}")
                break

        if not row_found:
            logger.info("No existing row found, appending new row...")
            rows.append(row_data)
            logger.info(f"Appended row: {row_data}")

        logger.info(f"Total rows to write: {len(rows)}")

        # Write back to file
        logger.info(f"Opening file for writing: {self._report_file_path}")
        try:
            with open(self._report_file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(rows)
            logger.info(f"Report file updated successfully: {self._report_file_path}")
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"Error writing report file: {e}")
            logger.exception("Full exception details:")
            QMessageBox.critical(
                self,
                "Report File Error",
                f"Failed to write to report file:\n{str(e)}"
            )
            logger.info("=" * 60)
