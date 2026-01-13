"""
Simple scanner that reads channels one by one without CS1016 scan mode.
This is a fallback for devices that don't support scan mode.
"""

import time
import logging
from typing import Dict, Optional
from PySide6.QtCore import QMutex, QMutexLocker

logger = logging.getLogger(__name__)


class SimpleChannelScanner:
    """
    Simple scanner that reads channels sequentially without using scan mode.
    """
    
    def __init__(self, device):
        """
        Initialize simple scanner.
        
        Args:
            device: Device interface (VisaInterface or VisaSimulator)
        """
        self._device = device
        self._running = False
        self._mutex = QMutex()
        self._interval = 2000  # Default 2 seconds
        
    def set_interval(self, interval_ms: int) -> None:
        """Set the scan interval."""
        with QMutexLocker(self._mutex):
            self._interval = interval_ms
            logger.debug(f"Scan interval set to {interval_ms}ms")
    
    def start_scanning(self, on_scan_complete, on_scan_error, on_channel_read, on_scan_started, on_scan_stopped) -> None:
        """Start continuous scanning loop."""
        with QMutexLocker(self._mutex):
            if self._running:
                logger.warning("Scanning already running")
                return
            self._running = True
        
        on_scan_started()
        logger.info("Simple scanner started")
        
        # Run continuous scan loop
        while True:
            with QMutexLocker(self._mutex):
                if not self._running:
                    break
                interval = self._interval
            
            # Perform scan
            try:
                if not self._device.is_connected():
                    error_msg = "Device not connected"
                    logger.error(error_msg)
                    on_scan_error(error_msg)
                    break
                
                # Read all channels one by one
                measurements = {}
                for channel_num in range(1, 17):
                    # Switch to channel
                    if hasattr(self._device, 'switch_channel'):
                        self._device.switch_channel(channel_num)
                        time.sleep(0.1)  # Wait for channel to settle
                    
                    # Read measurement
                    value = self._device.read_measurement()
                    measurements[channel_num] = value
                    
                    # Emit individual channel read for progress feedback
                    if value is not None:
                        on_channel_read(channel_num, value)
                
                # Emit results
                on_scan_complete(measurements)
                logger.debug(f"Scan completed: {len(measurements)} channels read")
                
            except Exception as e:
                error_msg = f"Scan error: {str(e)}"
                logger.error(error_msg)
                on_scan_error(error_msg)
                break
            
            # Wait for interval
            time.sleep(interval / 1000.0)
        
        # Emit scan_stopped when loop exits
        on_scan_stopped()
        logger.info("Simple scanner stopped")
    
    def stop_scanning(self) -> None:
        """Stop continuous scanning loop."""
        with QMutexLocker(self._mutex):
            if not self._running:
                logger.warning("Scanning not running")
                return
            self._running = False
        
        logger.info("Simple scanner stop requested")
