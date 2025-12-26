"""
VISA interface for SDM4055A-SC multimeter communication.
"""

import pyvisa
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class VisaInterface:
    """Interface for communicating with SDM4055A-SC multimeter via VISA."""

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
            return True
        except pyvisa.Error as e:
            logger.error(f"VISA write error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during function set: {e}")
            return False
