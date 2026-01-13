"""
Simulator for SDM4055A-SC multimeter (mock device for development).
"""

import random
import time
from typing import Optional, Dict, List
import logging
from PySide6.QtCore import QMutex, QMutexLocker

from .visa_interface import MeasurementType, ChannelConfig

logger = logging.getLogger(__name__)


class VisaSimulator:
    """Simulator class that mocks the API of VisaInterface for development without hardware."""

    def __init__(self, resource_string: str = ""):
        """
        Initialize simulator.

        Args:
            resource_string: Ignored in simulator mode (kept for API compatibility).
        """
        self.resource_string = resource_string
        self._connected = False

        # Mutex for thread-safe access
        self._mutex = QMutex()

        # Current measurement function
        self._current_function = "VOLT:DC"

        # Channel configurations (1-16)
        self._channel_configs: Dict[int, ChannelConfig] = {}
        self._initialize_channels()

        # Base values for different measurement types
        self._base_values = {
            MeasurementType.VOLTAGE_DC: 5.0,
            MeasurementType.VOLTAGE_AC: 3.5,
            MeasurementType.CURRENT_DC: 0.5,
            MeasurementType.CURRENT_AC: 0.3,
            MeasurementType.RESISTANCE_2WIRE: 100.0,
            MeasurementType.RESISTANCE_4WIRE: 100.0,
            MeasurementType.CAPACITANCE: 1.0e-6,
            MeasurementType.FREQUENCY: 1000.0,
            MeasurementType.DIODE: 0.7,
            MeasurementType.CONTINUITY: 0.0,
            MeasurementType.TEMP_RTD: 25.0,
            MeasurementType.TEMP_THERMOCOUPLE: 25.0,
        }
        self._noise_level = 0.1  # Noise level for simulated readings

    def connect(self) -> bool:
        """
        Simulate connection to the multimeter.

        Returns:
            True (always successful in simulator mode).
        """
        with QMutexLocker(self._mutex):
            self._connected = True
            logger.info("Simulator: Connected (mock device)")
            return True

    def disconnect(self) -> None:
        """Simulate disconnection from the multimeter."""
        with QMutexLocker(self._mutex):
            self._connected = False
            logger.info("Simulator: Disconnected")

    def is_connected(self) -> bool:
        """Check if device is connected."""
        with QMutexLocker(self._mutex):
            return self._connected

    def read_measurement(self) -> Optional[float]:
        """
        Simulate reading measurement value from the device.

        Returns:
            Simulated measurement value as float, or None if not connected.
        """
        if not self._connected:
            logger.warning("Simulator: Attempted to read while not connected")
            return None

        try:
            # Generate simulated reading with small random fluctuations
            # Use DC voltage as default measurement type
            base_value = self._base_values.get(MeasurementType.VOLTAGE_DC, 5.0)
            noise = random.uniform(-self._noise_level, self._noise_level)
            value = base_value + noise
            logger.debug(f"Simulator: Read value {value:.6f} V")
            return value
        except Exception as e:
            logger.error(f"Simulator: Unexpected error during read: {e}")
            return None

    def set_measurement_function(self, function: str = "VOLT:DC") -> bool:
        """
        Simulate setting the measurement function.

        Args:
            function: Measurement function (ignored in simulator mode).

        Returns:
            True (always successful in simulator mode).
        """
        self._current_function = function
        logger.info(f"Simulator: Set function to {function}")
        return True

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
            logger.error(f"Simulator: Invalid channel number: {channel_num}")
            return False

        # Validate measurement type based on channel
        if channel_num <= 12:
            # Channels 1-12 support all types except current
            if measurement_type in [MeasurementType.CURRENT_DC, MeasurementType.CURRENT_AC]:
                logger.error(
                    f"Simulator: Current measurement not supported on channel {channel_num}")
                return False
        else:
            # Channels 13-16 only support current
            if measurement_type not in [MeasurementType.CURRENT_DC, MeasurementType.CURRENT_AC]:
                logger.error(
                    f"Simulator: Only current measurement supported on channel {channel_num}")
                return False

        self._channel_configs[channel_num].measurement_type = measurement_type
        logger.info(
            f"Simulator: Set channel {channel_num} to {measurement_type.value}")
        return True

    def switch_channel(self, channel_num: int) -> bool:
        """
        Simulate switching to a specific channel.

        Args:
            channel_num: Channel number (1-16).

        Returns:
            True (always successful in simulator mode).
        """
        if channel_num < 1 or channel_num > 16:
            logger.error(f"Simulator: Invalid channel number: {channel_num}")
            return False

        logger.debug(f"Simulator: Switched to channel {channel_num}")
        return True

    def read_channel_measurement(self, channel_num: int) -> Optional[float]:
        """
        Simulate reading measurement from a specific channel.

        Args:
            channel_num: Channel number (1-16).

        Returns:
            Simulated measurement value as float, or None if read failed.
        """
        if not self._connected:
            logger.warning("Simulator: Attempted to read while not connected")
            return None

        if channel_num < 1 or channel_num > 16:
            logger.error(f"Simulator: Invalid channel number: {channel_num}")
            return None

        config = self._channel_configs.get(channel_num)
        if not config:
            logger.error(
                f"Simulator: No configuration for channel {channel_num}")
            return None

        try:
            # Generate simulated reading with small random fluctuations
            base_value = self._base_values.get(config.measurement_type, 0.0)
            noise = random.uniform(-self._noise_level, self._noise_level)
            value = base_value + noise
            logger.debug(
                f"Simulator: Read value {value:.6f} from channel {channel_num}")
            return value
        except Exception as e:
            logger.error(
                f"Simulator: Unexpected error during read on channel {channel_num}: {e}")
            return None

    def read_all_channels(self) -> Dict[int, Optional[float]]:
        """
        Simulate reading measurements from all 16 channels sequentially.

        Returns:
            Dictionary mapping channel numbers to simulated measurement values.
        """
        with QMutexLocker(self._mutex):
            results = {}
            for channel_num in range(1, 17):
                results[channel_num] = self.read_channel_measurement(
                    channel_num)
            return results

    def get_device_address(self) -> str:
        """
        Get the simulated USB device address.

        Returns:
            Device address string, or "Not connected" if not connected.
        """
        if not self._connected:
            return "Not connected"
        return "USB0::0x1AB1::0x04CE::SIMULATOR::INSTR"

    def get_device_info(self) -> Dict[str, str]:
        """
        Get simulated device information.

        Returns:
            Dictionary with simulated device information.
        """
        if not self._connected:
            return {}

        return {
            'manufacturer': 'SIGLENT',
            'model': 'SDM4055A-SC',
            'serial_number': 'SIMULATOR',
            'version': '1.00',
            'address': self.resource_string,
            'idn': 'SIGLENT,SDM4055A-SC,SIMULATOR,1.00'
        }

    def list_available_resources(self) -> List[str]:
        """
        List simulated available VISA resources.

        Returns:
            List of simulated VISA resource strings.
        """
        with QMutexLocker(self._mutex):
            # Return a mock list of resources
            return [
                "USB0::0x1AB1::0x04CE::SIMULATOR::INSTR"
            ]

    def get_measurement_function(self) -> str:
        """
        Get current measurement function.

        Returns:
            Current measurement function string.
        """
        return self._current_function
