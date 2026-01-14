"""
Main application window for SDM4055A-SC multimeter controller.
"""
import logging
from typing import Dict, List, Optional

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QAction
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
)

from hardware.visa_interface import VisaInterface, MeasurementType
from hardware.async_worker import AsyncScanManager
from hardware.simulator import VisaSimulator
from gui.widgets import ChannelIndicator

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    # Signals for thread-safe UI updates
    status_updated = Signal(str)
    connection_changed = Signal(bool)
    scan_started = Signal()
    scan_complete = Signal(object)

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """Initialize main window."""
        super().__init__(parent)
        self.setWindowTitle("SDM4055A-SC Multimeter Controller")
        self.resize(1200, 800)

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

        # Setup UI
        self._setup_ui()
        self._setup_connections()

        # Initialize default channel measurement types
        self._initialize_channel_measurement_types()

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

        self.btn_single_scan = QPushButton("Single Scan")
        self.btn_single_scan.clicked.connect(self._single_scan)
        self.btn_single_scan.setEnabled(False)

        self.btn_start_scan = QPushButton("Start Scan")
        self.btn_start_scan.clicked.connect(self._start_scanning)
        self.btn_start_scan.setEnabled(False)

        self.btn_stop_scan = QPushButton("Stop Scan")
        self.btn_stop_scan.clicked.connect(self._stop_scanning)
        self.btn_stop_scan.setEnabled(False)

        self.lbl_scan_status = QLabel("Ready to scan")

        scan_layout.addWidget(self.btn_single_scan)
        scan_layout.addWidget(self.btn_start_scan)
        scan_layout.addWidget(self.btn_stop_scan)
        scan_layout.addWidget(self.lbl_scan_status)
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

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self.status_updated.connect(self.status_bar.showMessage)
        self.connection_changed.connect(self._on_connection_changed)
        self.scan_started.connect(self._on_scan_started)
        self.scan_complete.connect(self._on_scan_complete)

        # Connect channel measurement type change signals
        for indicator in self.channel_indicators:
            indicator.measurement_type_changed.connect(
                self._on_channel_measurement_type_changed)

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
        """Initialize default measurement types for all channels."""
        for i in range(1, 17):
            if i <= 12:
                # Channels 1-12: default to DC voltage
                self._channel_measurement_types[i] = MeasurementType.VOLTAGE_DC.value
            else:
                # Channels 13-16: default to DC current
                self._channel_measurement_types[i] = MeasurementType.CURRENT_DC.value

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

    def get_all_channel_measurement_types(self) -> Dict[int, str]:
        """
        Get measurement types for all channels.

        Returns:
            Dictionary mapping channel numbers to measurement type strings.
        """
        return self._channel_measurement_types.copy()

    @Slot(bool)
    def _on_connection_changed(self, connected: bool) -> None:
        """Handle connection state change."""
        if not connected:
            # Reset all channel indicators
            for indicator in self.channel_indicators:
                indicator.reset_status()

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

        # Configure device with channel measurement types
        channel_configs = self.get_all_channel_measurement_types()
        if not self.scan_manager.configure_channels(channel_configs):
            QMessageBox.warning(self, "Configuration Error",
                                "Failed to configure channels with measurement types")
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
        self.lbl_scan_status.setText("Scanning...")
        QApplication.processEvents()

        # Create temporary scan manager for single scan
        temp_scan_manager = AsyncScanManager(device_interface)

        # Configure device with channel measurement types
        channel_configs = self.get_all_channel_measurement_types()
        if not temp_scan_manager.configure_channels(channel_configs):
            QMessageBox.warning(self, "Configuration Error",
                                "Failed to configure channels with measurement types")
            return

        # Connect signals
        temp_scan_manager.scan_complete.connect(self._on_single_scan_complete)

        # Perform single scan
        temp_scan_manager.perform_single_scan()
        logger.info("Single scan initiated")

    @Slot()
    def _on_scan_started(self) -> None:
        """Handle scan started signal."""
        self.btn_start_scan.setEnabled(False)
        self.btn_stop_scan.setEnabled(True)
        self.btn_single_scan.setEnabled(True)
        self.lbl_scan_status.setText("Scanning...")
        self.status_updated.emit("Scanning started")

    @Slot(object)
    def _on_scan_complete(self, measurements) -> None:
        """Handle scan complete signal.

        Args:
            measurements: Dictionary mapping channel numbers to measured values
        """
        logger.info(f"Scan complete. Measurements: {measurements}")

        # Update all channel indicators with new measurements
        for channel_num, value in measurements.items():
            if 1 <= channel_num <= 16:
                indicator = self.channel_indicators[channel_num - 1]
                indicator.set_value(value)

        # Update status
        self.lbl_scan_status.setText(
            f"Scan complete - {len(measurements)} channels")
        self.status_updated.emit(
            f"Scan complete - {len(measurements)} channels measured")

    @Slot()
    def _on_scan_stopped(self) -> None:
        """Handle scan stopped signal."""
        self.btn_start_scan.setEnabled(True)
        self.btn_stop_scan.setEnabled(False)
        self.btn_single_scan.setEnabled(True)
        self.lbl_scan_status.setText("Scan stopped")
        self.status_updated.emit("Scanning stopped")
        logger.info("Scan stopped, UI updated")

    @Slot(object)
    def _on_single_scan_complete(self, measurements) -> None:
        """Handle single scan complete signal.

        Args:
            measurements: Dictionary mapping channel numbers to measured values
        """
        logger.info(f"Single scan complete. Measurements: {measurements}")

        # Update all channel indicators with new measurements
        for channel_num, value in measurements.items():
            if 1 <= channel_num <= 16:
                indicator = self.channel_indicators[channel_num - 1]
                indicator.set_value(value)

        # Update status
        self.lbl_scan_status.setText(
            f"Scan complete - {len(measurements)} channels")
        self.status_updated.emit(
            f"Single scan complete - {len(measurements)} channels measured")

    @Slot(int, float)
    def _on_channel_read(self, channel_num: int, value: float) -> None:
        """Handle individual channel read signal.

        Args:
            channel_num: Channel number (1-16)
            value: Measured value
        """
        logger.debug(f"Channel {channel_num} read: {value}")

        # Only update indicator if scan is still running
        # Don't set status here - let _on_scan_complete handle final display
        if 1 <= channel_num <= 16:
            indicator = self.channel_indicators[channel_num - 1]
            # Just update value, don't set status
            indicator.set_value(value)

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
