"""
VISA interface for SDM4055A-SC multimeter communication.
"""

import pyvisa
from typing import Optional, Dict, List
import logging
import time
from enum import Enum
from PySide6.QtCore import QMutex, QMutexLocker

logger = logging.getLogger(__name__)


class MeasurementType(Enum):
    """Enumeration of supported measurement types."""
    VOLTAGE_DC = "VOLT:DC"
    VOLTAGE_AC = "VOLT:AC"
    CURRENT_DC = "CURR:DC"
    CURRENT_AC = "CURR:AC"
    RESISTANCE_2WIRE = "RES"
    RESISTANCE_4WIRE = "FRES"
    CAPACITANCE = "CAP"
    FREQUENCY = "FREQ"
    DIODE = "DIOD"
    CONTINUITY = "CONT"
    TEMP_RTD = "TEMP:RTD"
    TEMP_THERMOCOUPLE = "TEMP:THER"


class ChannelConfig:
    """Configuration for a single channel."""
    
    def __init__(self, channel_num: int, measurement_type: MeasurementType = MeasurementType.VOLTAGE_DC):
        """
        Initialize channel configuration.
        
        Args:
            channel_num: Channel number (1-16).
            measurement_type: Measurement type for this channel.
        """
        self.channel_num = channel_num
        self.measurement_type = measurement_type


class VisaInterface:
    """Interface for communicating with SDM4055A-SC multimeter via VISA with CS1016 scanning card support."""

    def __init__(self, resource_string: str = ""):
        """
        Initialize VISA interface.

        Args:
            resource_string: VISA resource string (e.g., "USB0::0x1AB1::0x04CE::DS1234567890::INSTR")
                             If empty, will auto-detect first available USB device.
        """
        self.resource_string = resource_string
        self.rm: Optional[pyvisa.ResourceManager] = None
        self.instrument: Optional[pyvisa.resources.MessageBasedResource] = None
        self._connected = False
        self._scan_mode_enabled = False
        
        # Mutex for thread-safe access to device
        self._mutex = QMutex()
        
        # Channel configurations (1-16)
        self._channel_configs: Dict[int, ChannelConfig] = {}
        self._initialize_channels()

    def connect(self) -> bool:
        """
        Establish connection to multimeter.

        Returns:
            True if connection successful, False otherwise.
        """
        with QMutexLocker(self._mutex):
            try:
                self.rm = pyvisa.ResourceManager()

                # Auto-detect device if resource string not provided
                if not self.resource_string:
                    resources = self.rm.list_resources()
                    if not resources:
                        logger.error("No VISA resources found")
                        return False
                    # Use first USB resource
                    self.resource_string = next((r for r in resources if "USB" in r), resources[0])
                    logger.info(f"Auto-detected resource: {self.resource_string}")

                self.instrument = self.rm.open_resource(self.resource_string)
                self.instrument.timeout = 2000  # 2 second timeout

                # Send identification query to verify connection
                idn = self.instrument.query("*IDN?")
                logger.info(f"Connected to: {idn.strip()}")

                self._connected = True
                return True

            except pyvisa.Error as e:
                logger.error(f"VISA connection error: {e}")
                self._connected = False
                return False
            except Exception as e:
                logger.error(f"Unexpected error during connection: {e}")
                self._connected = False
                return False

    def disconnect(self) -> None:
        """Terminate connection to multimeter."""
        with QMutexLocker(self._mutex):
            try:
                if self.instrument:
                    self.instrument.close()
                    self.instrument = None
                if self.rm:
                    self.rm.close()
                    self.rm = None
                self._connected = False
                self._scan_mode_enabled = False
                logger.info("Disconnected from device")
            except Exception as e:
                logger.error(f"Error during disconnection: {e}")

    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self._connected

    def read_measurement(self) -> Optional[float]:
        """
        Read measurement value from device.

        Returns:
            Measurement value as float, or None if read failed.
        """
        with QMutexLocker(self._mutex):
            if not self._connected or not self.instrument:
                logger.warning("Attempted to read while not connected")
                return None

            try:
                # Query measurement value
                value_str = self.instrument.query(":MEAS:VOLT:DC?")
                value = float(value_str.strip())
                return value
            except pyvisa.Error as e:
                logger.error(f"VISA read error: {e}")
                return None
            except ValueError as e:
                logger.error(f"Value conversion error: {e}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error during read: {e}")
                return None

    def set_measurement_function(self, function: str = "VOLT:DC") -> bool:
        """
        Set the measurement function.

        Args:
            function: Measurement function (e.g., "VOLT:DC", "CURR:DC", "RES")

        Returns:
            True if successful, False otherwise.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to set function while not connected")
            return False

        try:
            self.instrument.write(f":CONF:{function}")
            # Add delay to allow measurement function to settle
            time.sleep(0.05)  # 50ms delay for function settling
            return True
        except pyvisa.Error as e:
            logger.error(f"VISA write error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during function set: {e}")
            return False

    def _initialize_channels(self) -> None:
        """Initialize default channel configurations for all 16 channels."""
        for i in range(1, 17):
            # Channels 1-12: default to DC voltage
            # Channels 13-16: default to DC current
            if i <= 12:
                default_type = MeasurementType.VOLTAGE_DC
            else:
                default_type = MeasurementType.CURRENT_DC
            self._channel_configs[i] = ChannelConfig(i, default_type)

    def get_channel_config(self, channel_num: int) -> Optional[ChannelConfig]:
        """
        Get configuration for a specific channel.

        Args:
            channel_num: Channel number (1-16).

        Returns:
            ChannelConfig if valid channel, None otherwise.
        """
        return self._channel_configs.get(channel_num)

    def set_channel_measurement_type(self, channel_num: int, measurement_type: MeasurementType) -> bool:
        """
        Set the measurement type for a specific channel.

        Args:
            channel_num: Channel number (1-16).
            measurement_type: Measurement type to set.

        Returns:
            True if successful, False otherwise.
        """
        if channel_num < 1 or channel_num > 16:
            logger.error(f"Invalid channel number: {channel_num}")
            return False

        # Validate measurement type based on channel
        if channel_num <= 12:
            # Channels 1-12 support all types except current
            if measurement_type in [MeasurementType.CURRENT_DC, MeasurementType.CURRENT_AC]:
                logger.error(f"Current measurement not supported on channel {channel_num}")
                return False
        else:
            # Channels 13-16 only support current
            if measurement_type not in [MeasurementType.CURRENT_DC, MeasurementType.CURRENT_AC]:
                logger.error(f"Only current measurement supported on channel {channel_num}")
                return False

        self._channel_configs[channel_num].measurement_type = measurement_type
        logger.info(f"Set channel {channel_num} to {measurement_type.value}")
        return True

    def enable_scan_mode(self) -> bool:
        """
        Enable CS1016 scan mode.

        Returns:
            True if successful, False otherwise.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to enable scan mode while not connected")
            return False

        try:
            # Enable scan mode
            self.instrument.write(":ROUT:SCAN ON")
            time.sleep(0.2)  # 200ms delay for mode to settle
            
            # Set scan function to STEP
            self.instrument.write(":ROUT:FUNC STEP")
            time.sleep(0.1)  # 100ms delay
            
            # Turn off auto-zero for faster scanning (optional)
            self.instrument.write(":ROUT:DCV:AZ OFF")
            time.sleep(0.1)  # 100ms delay
            
            self._scan_mode_enabled = True
            logger.info("Scan mode enabled")
            return True
        except pyvisa.Error as e:
            logger.error(f"VISA scan mode enable error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during scan mode enable: {e}")
            return False

    def configure_scan_channel(self, channel_num: int) -> bool:
        """
        Configure a specific channel for scanning.

        Args:
            channel_num: Channel number (1-16).

        Returns:
            True if successful, False otherwise.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to configure channel while not connected")
            return False

        if channel_num < 1 or channel_num > 16:
            logger.error(f"Invalid channel number: {channel_num}")
            return False

        config = self._channel_configs.get(channel_num)
        if not config:
            logger.error(f"No configuration for channel {channel_num}")
            return False

        try:
            # Convert MeasurementType to CS1016 channel type
            type_map = {
                MeasurementType.VOLTAGE_DC: "DCV",
                MeasurementType.VOLTAGE_AC: "ACV",
                MeasurementType.CURRENT_DC: "DCA",
                MeasurementType.CURRENT_AC: "ACA",
                MeasurementType.RESISTANCE_2WIRE: "RES",
                MeasurementType.RESISTANCE_4WIRE: "RES",
                MeasurementType.CAPACITANCE: "CAP",
                MeasurementType.FREQUENCY: "FREQ",
                MeasurementType.DIODE: "DIOD",
                MeasurementType.CONTINUITY: "CONT",
                MeasurementType.TEMP_RTD: "RTD",
                MeasurementType.TEMP_THERMOCOUPLE: "THER",
            }
            
            channel_type = type_map.get(config.measurement_type, "DCV")
            
            # Configure channel: ROUT:CHAN <ch>,ON,<type>,AUTO,FAST
            cmd = f":ROUT:CHAN {channel_num},ON,{channel_type},AUTO,FAST"
            self.instrument.write(cmd)
            time.sleep(0.05)  # 50ms delay
            
            logger.debug(f"Configured channel {channel_num} as {channel_type}")
            return True
        except pyvisa.Error as e:
            logger.error(f"VISA channel configuration error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during channel configuration: {e}")
            return False

    def configure_all_scan_channels(self) -> bool:
        """
        Configure all channels for scanning.

        Returns:
            True if successful, False otherwise.
        """
        for channel_num in range(1, 17):
            if not self.configure_scan_channel(channel_num):
                logger.error(f"Failed to configure channel {channel_num}")
                return False
            # Add delay between channel configurations
            time.sleep(0.1)  # 100ms delay between channels
        return True

    def set_scan_limits(self, low: int = 1, high: int = 16) -> bool:
        """
        Set scan limits (channel range).

        Args:
            low: Lowest channel number (1-16).
            high: Highest channel number (1-16).

        Returns:
            True if successful, False otherwise.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to set scan limits while not connected")
            return False

        if low < 1 or low > 16 or high < 1 or high > 16 or low > high:
            logger.error(f"Invalid scan limits: low={low}, high={high}")
            return False

        try:
            # Set high limit
            self.instrument.write(f":ROUT:LIMI:HIGH {high}")
            time.sleep(0.1)  # 100ms delay
            
            # Set low limit
            self.instrument.write(f":ROUT:LIMI:LOW {low}")
            time.sleep(0.1)  # 100ms delay
            
            logger.info(f"Set scan limits: {low} to {high}")
            return True
        except pyvisa.Error as e:
            logger.error(f"VISA scan limits error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during scan limits set: {e}")
            return False

    def start_scan(self) -> bool:
        """
        Start scanning.

        Returns:
            True if successful, False otherwise.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to start scan while not connected")
            return False

        try:
            # Set scan count to 1 (single scan)
            self.instrument.write(":ROUT:COUN 1")
            time.sleep(0.1)  # 100ms delay
            
            # Start scan
            self.instrument.write(":ROUT:START ON")
            time.sleep(0.2)  # 200ms delay for scan to start
            
            logger.info("Scan started")
            return True
        except pyvisa.Error as e:
            logger.error(f"VISA scan start error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during scan start: {e}")
            return False

    def is_scan_complete(self) -> bool:
        """
        Check if scan is complete.

        Returns:
            True if scan is complete, False if still scanning.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to check scan status while not connected")
            return False

        try:
            # Query scan status
            response = self.instrument.query(":ROUT:START?")
            return response.strip() == "OFF"
        except pyvisa.Error as e:
            logger.error(f"VISA scan status error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during scan status check: {e}")
            return False

    def get_scan_data(self, channel_num: int) -> Optional[float]:
        """
        Get scan data for a specific channel.

        Args:
            channel_num: Channel number (1-16).

        Returns:
            Measurement value as float, or None if read failed.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to get scan data while not connected")
            return None

        if channel_num < 1 or channel_num > 16:
            logger.error(f"Invalid channel number: {channel_num}")
            return None

        try:
            # Query scan data for channel
            response = self.instrument.query(f":ROUT:DATA? {channel_num}")
            
            # Parse the response - it may contain unit suffix (e.g., "-4.24124300E-04 VDC")
            # Extract only the numeric part before any space
            value_str = response.strip().split()[0]
            value = float(value_str)
            return value
        except pyvisa.Error as e:
            logger.error(f"VISA scan data error on channel {channel_num}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value conversion error on channel {channel_num}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during scan data retrieval on channel {channel_num}: {e}")
            return None

    def read_all_channels(self) -> Dict[int, Optional[float]]:
        """
        Read measurements from all 16 channels using CS1016 scan mode.

        Returns:
            Dictionary mapping channel numbers to measurement values (or None if failed).
        """
        with QMutexLocker(self._mutex):
            if not self._connected or not self.instrument:
                logger.warning("Attempted to read while not connected")
                return {}

            try:
                # Enable scan mode if not already enabled
                if not self._scan_mode_enabled:
                    if not self.enable_scan_mode():
                        logger.error("Failed to enable scan mode")
                        return {}
                
                # Configure all channels
                if not self.configure_all_scan_channels():
                    logger.error("Failed to configure channels")
                    return {}
                
                # Set scan limits (all 16 channels)
                if not self.set_scan_limits(1, 16):
                    logger.error("Failed to set scan limits")
                    return {}
                
                # Start scan
                if not self.start_scan():
                    logger.error("Failed to start scan")
                    return {}
                
                # Wait for scan to complete
                max_wait_time = 30  # 30 seconds maximum wait time
                start_time = time.time()
                while time.time() - start_time < max_wait_time:
                    if self.is_scan_complete():
                        break
                    time.sleep(0.1)  # Poll every 100ms
                else:
                    logger.warning("Scan timeout - may not have completed")
                
                # Read data from all channels
                results = {}
                for channel_num in range(1, 17):
                    results[channel_num] = self.get_scan_data(channel_num)
                
                return results
            except Exception as e:
                logger.error(f"Unexpected error during multi-channel scan: {e}")
                return {}

    def get_device_address(self) -> str:
        """
        Get the USB device address.

        Returns:
            Device address string, or "Not connected" if not connected.
        """
        if not self._connected or not self.resource_string:
            return "Not connected"
        return self.resource_string
