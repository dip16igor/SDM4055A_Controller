"""
VISA interface for SDM4055A-SC multimeter communication.
"""

import pyvisa
from typing import Optional, Dict, List
import logging
import time
from enum import Enum

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

    # CS1016 card channel switching command format
    CS1016_CHANNEL_CMD = ":ROUT:CLOS (@{channel})"

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
        self._cs1016_detected = False
        
        # Channel configurations (1-16)
        self._channel_configs: Dict[int, ChannelConfig] = {}
        self._initialize_channels()

    def connect(self) -> bool:
        """
        Establish connection to the multimeter.

        Returns:
            True if connection successful, False otherwise.
        """
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
        """Terminate connection to the multimeter."""
        try:
            if self.instrument:
                self.instrument.close()
                self.instrument = None
            if self.rm:
                self.rm.close()
                self.rm = None
            self._connected = False
            logger.info("Disconnected from device")
        except Exception as e:
            logger.error(f"Error during disconnection: {e}")

    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self._connected

    def read_measurement(self) -> Optional[float]:
        """
        Read measurement value from the device.

        Returns:
            Measurement value as float, or None if read failed.
        """
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

    def switch_channel(self, channel_num: int) -> bool:
        """
        Switch to a specific channel using CS1016 card.

        Args:
            channel_num: Channel number (1-16).

        Returns:
            True if successful, False otherwise.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to switch channel while not connected")
            return False

        if channel_num < 1 or channel_num > 16:
            logger.error(f"Invalid channel number: {channel_num}")
            return False

        try:
            # Send channel switching command
            cmd = self.CS1016_CHANNEL_CMD.format(channel=channel_num)
            self.instrument.write(cmd)
            # Add delay to allow relay switching to complete
            time.sleep(0.1)  # 100ms delay for relay settling
            logger.debug(f"Switched to channel {channel_num}")
            return True
        except pyvisa.Error as e:
            logger.error(f"VISA channel switch error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during channel switch: {e}")
            return False

    def read_channel_measurement(self, channel_num: int) -> Optional[float]:
        """
        Read measurement from a specific channel.

        Args:
            channel_num: Channel number (1-16).

        Returns:
            Measurement value as float, or None if read failed.
        """
        if not self._connected or not self.instrument:
            logger.warning("Attempted to read while not connected")
            return None

        if channel_num < 1 or channel_num > 16:
            logger.error(f"Invalid channel number: {channel_num}")
            return None

        config = self._channel_configs.get(channel_num)
        if not config:
            logger.error(f"No configuration for channel {channel_num}")
            return None

        try:
            # Switch to channel
            if not self.switch_channel(channel_num):
                return None

            # Set measurement function for this channel
            if not self.set_measurement_function(config.measurement_type.value):
                return None

            # Add small delay before reading to allow measurement to stabilize
            time.sleep(0.05)  # 50ms delay for measurement stabilization

            # Read measurement
            value_str = self.instrument.query(f":MEAS:{config.measurement_type.value}?")
            value = float(value_str.strip())
            return value
        except pyvisa.Error as e:
            logger.error(f"VISA read error on channel {channel_num}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Value conversion error on channel {channel_num}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during read on channel {channel_num}: {e}")
            return None

    def read_all_channels(self) -> Dict[int, Optional[float]]:
        """
        Read measurements from all 16 channels sequentially.

        Returns:
            Dictionary mapping channel numbers to measurement values (or None if failed).
        """
        results = {}
        for channel_num in range(1, 17):
            results[channel_num] = self.read_channel_measurement(channel_num)
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
