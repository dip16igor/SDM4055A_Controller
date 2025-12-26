"""
Simulator for SDM4055A-SC multimeter (mock device for development).
"""

import random
import time
from typing import Optional
import logging

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
        self._base_value = 5.0  # Base voltage value for simulation
        self._noise_level = 0.1  # Noise level for simulated readings

    def connect(self) -> bool:
        """
        Simulate connection to the multimeter.

        Returns:
            True (always successful in simulator mode).
        """
        self._connected = True
        logger.info("Simulator: Connected (mock device)")
        return True

    def disconnect(self) -> None:
        """Simulate disconnection from the multimeter."""
        self._connected = False
        logger.info("Simulator: Disconnected")

    def is_connected(self) -> bool:
        """Check if device is connected."""
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
            noise = random.uniform(-self._noise_level, self._noise_level)
            value = self._base_value + noise
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
        logger.info(f"Simulator: Set function to {function}")
        return True
