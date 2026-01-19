"""
VISA interface for SDM4055A-SC multimeter communication.
"""

import pyvisa
from typing import Optional, Dict, List, Any
import logging
import time
from enum import Enum
from dataclasses import dataclass
from PySide6.QtCore import QMutex, QMutexLocker

logger = logging.getLogger(__name__)


@dataclass
class ScanDataResult:
    """Result from scanning a channel with unit information."""
    value: float
    unit: str  # Base unit (V, A, OHM, F, Hz, °C, etc.)
    full_unit: str  # Full unit string (VDC, VAC, ADC, AAC, OHM, etc.)
    range_info: str = ""  # Optional range information (e.g., "200mV", "2V", "AUTO")


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
    
    def __init__(self, channel_num: int, measurement_type: MeasurementType = MeasurementType.VOLTAGE_DC, range_value: str = "AUTO"):
        """
        Initialize channel configuration.
        
        Args:
            channel_num: Channel number (1-16).
            measurement_type: Measurement type for this channel.
            range_value: Measurement range (e.g., "200 mV", "AUTO").
        """
        self.channel_num = channel_num
        self.measurement_type = measurement_type
        self.range_value = range_value


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
        with QMutexLocker(self._mutex):
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

    # Mapping of range values to SCPI range commands (CS1016 supported ranges only)
    # IMPORTANT: CS1016 scanning card has DIFFERENT range limitations than the multimeter itself!
    # See doc/CS1016_Supported_Ranges.md for detailed information
    RANGE_TO_SCPI = {
        # Voltage ranges - CS1016 only supports up to 200V (1000V and 750V are NOT supported)
        "200 mV": "200mV",
        "2 V": "2V",
        "20 V": "20V",
        "200 V": "200V",
        # Current ranges - CS1016 ONLY supports 2A range (all other ranges are NOT supported)
        "2 A": "2A",
        # Capacitance ranges - 10000 uF is supported instead of 10 mF
        "2 nF": "2nF",
        "20 nF": "20nF",
        "200 nF": "200nF",
        "2 uF": "2uF",
        "20 uF": "20uF",
        "200 uF": "200uF",
        "10000 uF": "10000uF",
        # Resistance ranges
        "200 Ohm": "200OHM",
        "2 kOhm": "2kOHM",
        "20 kOhm": "20kOHM",
        "200 kOhm": "200kOHM",
        "2 MOhm": "2MOHM",
        "10 MOhm": "10MOHM",
        "100 MOhm": "100MOHM",
        # AUTO range
        "AUTO": "AUTO",
    }
    
    def _initialize_channels(self) -> None:
        """Initialize default channel configurations for all 16 channels."""
        for i in range(1, 17):
            # Channels 1-12: default to DC voltage
            # Channels 13-16: default to DC current
            if i <= 12:
                default_type = MeasurementType.VOLTAGE_DC
            else:
                default_type = MeasurementType.CURRENT_DC
            self._channel_configs[i] = ChannelConfig(i, default_type, "AUTO")

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
    
    def set_channel_range(self, channel_num: int, range_value: str) -> bool:
        """
        Set measurement range for a specific channel.

        Args:
            channel_num: Channel number (1-16).
            range_value: Range value (e.g., "200 mV", "AUTO").

        Returns:
            True if successful, False otherwise.
        """
        if channel_num < 1 or channel_num > 16:
            logger.error(f"Invalid channel number: {channel_num}")
            return False

        # Validate range value based on CS1016 scanning card limitations
        # IMPORTANT: CS1016 has different range limitations than the multimeter itself!
        # See doc/CS1016_Supported_Ranges.md for detailed information

        # Get the channel's measurement type to validate range compatibility
        config = self._channel_configs.get(channel_num)
        if not config:
            logger.error(f"No configuration for channel {channel_num}")
            return False

        # Define valid ranges for each measurement type (CS1016 supported ranges only)
        valid_ranges_by_type = {
            MeasurementType.VOLTAGE_DC: ["200 mV", "2 V", "20 V", "200 V", "AUTO"],
            MeasurementType.VOLTAGE_AC: ["200 mV", "2 V", "20 V", "200 V", "AUTO"],
            MeasurementType.CURRENT_DC: ["2 A"],  # CS1016 only supports 2A for current
            MeasurementType.CURRENT_AC: ["2 A"],  # CS1016 only supports 2A for current
            MeasurementType.RESISTANCE_2WIRE: ["200 Ohm", "2 kOhm", "20 kOhm", "200 kOhm", "2 MOhm", "10 MOhm", "100 MOhm", "AUTO"],
            MeasurementType.RESISTANCE_4WIRE: ["200 Ohm", "2 kOhm", "20 kOhm", "200 kOhm", "2 MOhm", "10 MOhm", "100 MOhm", "AUTO"],
            MeasurementType.CAPACITANCE: ["2 nF", "20 nF", "200 nF", "2 uF", "20 uF", "200 uF", "10000 uF", "AUTO"],
            MeasurementType.FREQUENCY: ["AUTO"],
            MeasurementType.DIODE: ["AUTO"],
            MeasurementType.CONTINUITY: ["AUTO"],
            MeasurementType.TEMP_RTD: ["AUTO"],
            MeasurementType.TEMP_THERMOCOUPLE: ["AUTO"],
        }

        valid_ranges = valid_ranges_by_type.get(config.measurement_type, ["AUTO"])

        if range_value not in valid_ranges:
            logger.error(f"Invalid range value '{range_value}' for channel {channel_num} with measurement type {config.measurement_type.value}")
            logger.error(f"Valid ranges for {config.measurement_type.value} are: {', '.join(valid_ranges)}")
            logger.error("See doc/CS1016_Supported_Ranges.md for detailed information about CS1016 limitations")
            return False

        self._channel_configs[channel_num].range_value = range_value
        logger.info(f"Set channel {channel_num} range to {range_value}")
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
            logger.info("Sending: :ROUT:SCAN ON")
            self.instrument.write(":ROUT:SCAN ON")
            time.sleep(0.2)  # 200ms delay for mode to settle
            
            # Set scan function to STEP
            logger.info("Sending: :ROUT:FUNC STEP")
            self.instrument.write(":ROUT:FUNC STEP")
            time.sleep(0.1)  # 100ms delay
            
            # Turn off auto-zero for faster scanning (optional)
            logger.info("Sending: :ROUT:DCV:AZ OFF")
            self.instrument.write(":ROUT:DCV:AZ OFF")
            time.sleep(0.1)  # 100ms delay
            
            self._scan_mode_enabled = True
            logger.info("Scan mode enabled successfully")
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
                MeasurementType.CURRENT_DC: "DCI",  # DCI (not DCA) for DC current
                MeasurementType.CURRENT_AC: "ACI",  # ACI (not ACA) for AC current
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
            
            # Get SCPI range command from range value
            range_scpi = self.RANGE_TO_SCPI.get(config.range_value, "AUTO")
            
            # Determine speed based on measurement type and range
            # Current measurements (DCI, ACI) must use SLOW speed
            # 200 mV range also requires SLOW speed to avoid errors
            if channel_type in ["DCI", "ACI"] or range_scpi == "200mV":
                speed = "SLOW"
            else:
                speed = "FAST"
            
            # Configure channel: ROUT:CHAN <ch>,ON,<type>,<range>,<speed>
            cmd = f":ROUT:CHAN {channel_num},ON,{channel_type},{range_scpi},{speed}"
            logger.info(f"Configuring channel {channel_num}: {cmd}")
            self.instrument.write(cmd)
            time.sleep(0.05)  # 50ms delay
            
            # Check for errors after configuration
            try:
                # Query system error status to detect configuration errors
                error_response = self.instrument.query(":SYST:ERR?")
                error_response = error_response.strip()
                if error_response and error_response != '0,"No error"':
                    logger.error(f"Channel {channel_num} configuration error: {error_response}")
                    # Log additional details
                    try:
                        error_query = self.instrument.query(":SYST:ERR?")
                        logger.error(f"Error details: {error_query.strip()}")
                    except:
                        pass
            except pyvisa.Error as e:
                logger.warning(f"Could not query error status: {e}")
            
            logger.debug(f"Configured channel {channel_num} as {channel_type} with range {range_scpi}")
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
            time.sleep(1.0)  # 1 second delay between channels for device to settle
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
            logger.info("Sending: :ROUT:COUN 1")
            self.instrument.write(":ROUT:COUN 1")
            time.sleep(0.1)  # 100ms delay
            
            # Start scan
            logger.info("Sending: :ROUT:START ON")
            self.instrument.write(":ROUT:START ON")
            time.sleep(0.2)  # 200ms delay for scan to start
            
            logger.info("Scan started successfully")
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

    def get_scan_data(self, channel_num: int) -> Optional[ScanDataResult]:
        """
        Get scan data for a specific channel with unit information.

        Args:
            channel_num: Channel number (1-16).

        Returns:
            ScanDataResult with value, unit, and full_unit, or None if read failed.
            If the measurement is overloaded, returns ScanDataResult with is_overload=True.
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
            
            logger.debug(f"Channel {channel_num} raw response: {response.strip()}")
            
            # Check if response contains overload indicator
            # The multimeter may return "9.9e+37" or similar large value when overloaded
            # or it may return a string like "overloadDC"
            response_stripped = response.strip()
            
            # Check for overload conditions
            if "overload" in response_stripped.lower():
                # Extract the overload message (e.g., "overloadDC")
                overload_msg = response_stripped
                logger.warning(f"Channel {channel_num}: Overload detected - {overload_msg}")
                return ScanDataResult(
                    value=0.0,
                    unit="OVERLOAD",
                    full_unit=overload_msg,
                    range_info="OVERLOAD"
                )
            
            # Parse the response - it may contain unit suffix (e.g., "-4.24124300E-04 VDC")
            # Extract only the numeric part before any space
            parts = response_stripped.split()
            
            if not parts:
                logger.error(f"Channel {channel_num}: Empty response")
                return None
            
            value_str = parts[0]
            
            try:
                value = float(value_str)
                
                # Check if value is extremely large (indicates overload)
                # The multimeter typically sends 9.9e+37 when overloaded
                OVERLOAD_THRESHOLD = 1e35  # Threshold to detect overload
                if abs(value) > OVERLOAD_THRESHOLD:
                    logger.warning(f"Channel {channel_num}: Overload detected (value={value})")
                    # Construct appropriate overload message based on measurement type
                    # Try to get the full unit from the response if available
                    if len(parts) > 1:
                        # Extract the measurement type from the unit suffix (e.g., "VDC" -> "DC")
                        unit_suffix = parts[1]
                        # Create overload message by replacing the value part with "overload"
                        overload_msg = f"overload{unit_suffix[1:]}" if len(unit_suffix) > 1 else "OVERLOAD"
                    else:
                        overload_msg = "OVERLOAD"
                    return ScanDataResult(
                        value=0.0,
                        unit="OVERLOAD",
                        full_unit=overload_msg,
                        range_info="OVERLOAD"
                    )
                
                # Extract unit information from the response
                full_unit = parts[1] if len(parts) > 1 else ""
                
                # Map full unit to base unit
                unit_mapping = {
                    "VDC": "V", "VAC": "V",
                    "ADC": "A", "AAC": "A",
                    "OHM": "Ω", "OHMS": "Ω",
                    "F": "F",
                    "HZ": "Hz", "HERTZ": "Hz",
                    "DEGC": "°C", "DEGF": "°F",
                }
                
                base_unit = unit_mapping.get(full_unit, "")
                
                logger.debug(f"Channel {channel_num}: value={value}, full_unit={full_unit}, base_unit={base_unit}")
                
                return ScanDataResult(
                    value=value,
                    unit=base_unit,
                    full_unit=full_unit,
                    range_info=""
                )
                
            except ValueError as e:
                logger.error(f"Channel {channel_num}: Failed to convert '{value_str}' to float: {e}")
                return None
        except pyvisa.Error as e:
            logger.error(f"VISA scan data error on channel {channel_num}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value conversion error on channel {channel_num}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during scan data retrieval on channel {channel_num}: {e}")
            return None

    def read_all_channels(self) -> Dict[int, Optional[ScanDataResult]]:
        """
        Read measurements from all 16 channels.
        
        First tries CS1016 scan mode, falls back to channel-by-channel reading if scan mode fails.
        
        Returns:
            Dictionary mapping channel numbers to ScanDataResult objects (or None if failed).
            Each ScanDataResult contains value, unit, full_unit, and range_info.
        """
        with QMutexLocker(self._mutex):
            if not self._connected or not self.instrument:
                logger.warning("Attempted to read while not connected")
                return {}

            try:
                # Try scan mode first
                if not self._scan_mode_enabled:
                    logger.info("Attempting to enable scan mode...")
                    if not self.enable_scan_mode():
                        logger.warning("Scan mode failed, falling back to channel-by-channel reading")
                        return self._read_channels_sequentially()
                
                # Configure all channels
                if not self.configure_all_scan_channels():
                    logger.warning("Channel configuration failed, falling back to sequential reading")
                    return self._read_channels_sequentially()
                
                # Set scan limits (all 16 channels)
                if not self.set_scan_limits(1, 16):
                    logger.warning("Scan limits failed, falling back to sequential reading")
                    return self._read_channels_sequentially()
                
                # Start scan
                if not self.start_scan():
                    logger.warning("Scan start failed, falling back to sequential reading")
                    return self._read_channels_sequentially()
                
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
                logger.info("Starting to read data from all 16 channels...")
                results = {}
                for channel_num in range(1, 17):
                    logger.info(f"About to call get_scan_data for channel {channel_num}")
                    results[channel_num] = self.get_scan_data(channel_num)
                    logger.info(f"Channel {channel_num} result: {results[channel_num]}")
                
                logger.info(f"read_all_channels returning {len(results)} results: {results}")
                return results
            except Exception as e:
                logger.error(f"Unexpected error during multi-channel scan: {e}")
                logger.info("Falling back to sequential channel reading")
                return self._read_channels_sequentially()
    
    def _read_channels_sequentially(self) -> Dict[int, Optional[ScanDataResult]]:
        """
        Read all channels sequentially (channel by channel) without scan mode.
        
        This is a fallback method for devices that don't support CS1016 scan mode.
        
        Returns:
            Dictionary mapping channel numbers to ScanDataResult objects (or None if failed).
        """
        logger.info("Reading channels sequentially...")
        results = {}
        
        for channel_num in range(1, 17):
            try:
                # Switch to channel (if device supports it)
                # Note: SDM4055A-SC may not have channel switching commands
                # We'll just read from the current channel
                
                # Read measurement
                value = self.read_measurement()
                
                if value is not None:
                    # Convert float to ScanDataResult
                    # Note: Sequential reading doesn't provide unit information,
                    # so we use empty strings for unit fields
                    results[channel_num] = ScanDataResult(
                        value=value,
                        unit="",
                        full_unit="",
                        range_info=""
                    )
                else:
                    results[channel_num] = None
                
                logger.debug(f"Channel {channel_num}: {value}")
                
                # Small delay between channels
                time.sleep(0.05)  # 50ms
                
            except Exception as e:
                logger.error(f"Error reading channel {channel_num}: {e}")
                results[channel_num] = None
        
        logger.info(f"Sequential read completed: {len(results)} channels")
        return results

    def get_device_address(self) -> str:
        """
        Get the USB device address.

        Returns:
            Device address string, or "Not connected" if not connected.
        """
        if not self._connected or not self.resource_string:
            return "Not connected"
        return self.resource_string

    def list_available_resources(self) -> List[str]:
        """
        List all available VISA resources.

        Returns:
            List of VISA resource strings, or empty list if no resources found.
        """
        with QMutexLocker(self._mutex):
            # Create temporary resource manager if not initialized
            temp_rm = None
            try:
                if not self.rm:
                    logger.info("Creating temporary resource manager for listing resources")
                    temp_rm = pyvisa.ResourceManager()
                    rm_to_use = temp_rm
                else:
                    rm_to_use = self.rm
                
                resources = rm_to_use.list_resources()
                logger.info(f"Found {len(resources)} available VISA resources")
                return resources
            except pyvisa.Error as e:
                logger.error(f"Error listing VISA resources: {e}")
                return []
            except Exception as e:
                logger.error(f"Unexpected error listing resources: {e}")
                return []
            finally:
                # Clean up temporary resource manager if we created one
                if temp_rm is not None:
                    try:
                        temp_rm.close()
                        logger.debug("Closed temporary resource manager")
                    except Exception as e:
                        logger.warning(f"Error closing temporary resource manager: {e}")

    def get_device_info(self) -> Dict[str, str]:
        """
        Get detailed information about the connected device.

        Returns:
            Dictionary with device information keys:
            - manufacturer: Device manufacturer
            - model: Device model
            - serial_number: Device serial number
            - address: VISA resource address
            Or empty dict if not connected.
        """
        with QMutexLocker(self._mutex):
            if not self._connected or not self.instrument:
                logger.warning("Attempted to get device info while not connected")
                return {}
            
            try:
                # Query device identification
                idn = self.instrument.query("*IDN?").strip()
                
                # Parse IDN response (format: manufacturer,model,serial,version)
                parts = idn.split(',')
                
                device_info = {
                    'address': self.resource_string,
                    'idn': idn
                }
                
                if len(parts) >= 4:
                    device_info['manufacturer'] = parts[0].strip()
                    device_info['model'] = parts[1].strip()
                    device_info['serial_number'] = parts[2].strip()
                    device_info['version'] = parts[3].strip()
                elif len(parts) >= 1:
                    device_info['manufacturer'] = parts[0].strip()
                
                logger.info(f"Device info: {device_info}")
                return device_info
                
            except pyvisa.Error as e:
                logger.error(f"VISA error getting device info: {e}")
                return {}
            except Exception as e:
                logger.error(f"Unexpected error getting device info: {e}")
                return {}
