"""
Async worker thread for device operations to keep UI responsive.
"""

from PySide6.QtCore import QThread, Signal, QObject, QMutex, QMutexLocker
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ScanWorker(QObject):
    """
    Worker object that performs device scanning operations in a background thread.
    
    This worker runs in a separate QThread to prevent UI blocking during device I/O.
    All communication with main thread is done via Qt signals.
    """
    
    # Signals for communication with main thread
    scan_complete = Signal(object)  # Emitted when a full scan completes with results (using object for thread safety)
    scan_error = Signal(str)  # Emitted when an error occurs
    channel_read = Signal(int, float)  # Emitted when a single channel is read
    scan_started = Signal()  # Emitted when scanning starts
    scan_stopped = Signal()  # Emitted when scanning stops
    
    def __init__(self, device):
        """
        Initialize the scan worker.
        
        Args:
            device: Device interface (VisaInterface or VisaSimulator)
        """
        super().__init__()
        self._device = device
        self._running = False
        self._mutex = QMutex()
        self._interval = 2000  # Default 2 seconds
        
    def set_interval(self, interval_ms: int) -> None:
        """
        Set the scan interval.
        
        Args:
            interval_ms: Interval in milliseconds between scans.
        """
        with QMutexLocker(self._mutex):
            self._interval = interval_ms
            logger.debug(f"Scan interval set to {interval_ms}ms")
    
    def start_scanning(self) -> None:
        """Start continuous scanning loop."""
        with QMutexLocker(self._mutex):
            if self._running:
                logger.warning("Scanning already running")
                return
            self._running = True
        
        self.scan_started.emit()
        logger.info("Scan worker started")
        
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
                    self.scan_error.emit(error_msg)
                    break
                
                # Read all channels
                measurements = self._device.read_all_channels()
                
                # Emit results
                self.scan_complete.emit(measurements)
                
                # Also emit individual channel reads for progress feedback
                for channel_num, value in measurements.items():
                    if value is not None:
                        self.channel_read.emit(channel_num, value)
                
                logger.debug(f"Scan completed: {len(measurements)} channels read")
                
            except Exception as e:
                error_msg = f"Scan error: {str(e)}"
                logger.error(error_msg)
                self.scan_error.emit(error_msg)
                break
            
            # Wait for interval
            import time
            time.sleep(interval / 1000.0)
        
        # Emit scan_stopped when loop exits (either stopped or error)
        self.scan_stopped.emit()
        logger.info("Scan worker stopped")
    
    def stop_scanning(self) -> None:
        """Stop continuous scanning loop."""
        with QMutexLocker(self._mutex):
            if not self._running:
                logger.warning("Scanning not running")
                return
            self._running = False
        
        logger.info("Scan worker stop requested")


class AsyncScanManager(QObject):
    """
    Manager for async scanning operations.
    
    This class manages a QThread and ScanWorker to provide a clean interface
    for starting and stopping async scans.
    """
    
    # Signals for external connection
    scan_complete = Signal(object)
    scan_error = Signal(str)
    channel_read = Signal(int, float)
    scan_started = Signal()
    scan_stopped = Signal()
    
    def __init__(self, device):
        """
        Initialize the async scan manager.
        
        Args:
            device: Device interface (VisaInterface or VisaSimulator)
        """
        super().__init__()
        self._device = device
        self._thread: Optional[QThread] = None
        self._worker: Optional[ScanWorker] = None
        self._scanning = False
        
    def start(self, interval_ms: int = 2000) -> bool:
        """
        Start async scanning.
        
        Args:
            interval_ms: Scan interval in milliseconds.
            
        Returns:
            True if started successfully, False otherwise.
        """
        if self._scanning:
            logger.warning("Scanning already active")
            return False
        
        if not self._device.is_connected():
            logger.error("Cannot start scanning: device not connected")
            return False
        
        try:
            # Create thread and worker
            self._thread = QThread()
            self._worker = ScanWorker(self._device)
            self._worker.moveToThread(self._thread)
            
            # Set interval
            self._worker.set_interval(interval_ms)
            
            # Forward worker signals to manager signals
            self._worker.scan_complete.connect(self.scan_complete)
            self._worker.scan_error.connect(self.scan_error)
            self._worker.channel_read.connect(self.channel_read)
            self._worker.scan_started.connect(self.scan_started)
            self._worker.scan_stopped.connect(self._on_worker_scan_stopped)
            
            # Connect thread lifecycle
            self._thread.started.connect(self._worker.start_scanning)
            self._thread.finished.connect(self._on_thread_finished)
            
            # Start thread
            self._thread.start()
            self._scanning = True
            
            logger.info(f"Async scanning started with {interval_ms}ms interval")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start async scanning: {e}")
            self._cleanup()
            return False
    
    def stop(self) -> None:
        """Stop async scanning."""
        if not self._scanning:
            logger.warning("Scanning not active")
            return
        
        try:
            if self._worker:
                self._worker.stop_scanning()
            
            if self._thread:
                # Wait for thread to finish (with timeout)
                if not self._thread.wait(5000):  # 5 second timeout
                    logger.warning("Thread did not finish in time, forcing quit")
                    self._thread.quit()
                    self._thread.wait(1000)
            
            logger.info("Async scanning stopped")
            
        except Exception as e:
            logger.error(f"Error stopping async scanning: {e}")
            self._cleanup()
    
    def is_scanning(self) -> bool:
        """Check if scanning is active."""
        return self._scanning
    
    def perform_single_scan(self) -> None:
        """
        Perform a single scan of all channels without starting continuous scanning.
        
        This method executes a one-time scan and emits the scan_complete signal
        with the results. It runs synchronously in the calling thread.
        """
        if not self._device.is_connected():
            logger.error("Cannot perform single scan: device not connected")
            self.scan_error.emit("Device not connected")
            return
        
        try:
            # Read all channels
            measurements = self._device.read_all_channels()
            
            # Emit results
            self.scan_complete.emit(measurements)
            
            # Also emit individual channel reads for progress feedback
            for channel_num, value in measurements.items():
                if value is not None:
                    self.channel_read.emit(channel_num, value)
            
            logger.info(f"Single scan completed: {len(measurements)} channels read")
            
        except Exception as e:
            error_msg = f"Single scan error: {str(e)}"
            logger.error(error_msg)
            self.scan_error.emit(error_msg)
    
    def set_interval(self, interval_ms: int) -> None:
        """
        Update scan interval while scanning.
        
        Args:
            interval_ms: New interval in milliseconds.
        """
        if self._worker:
            self._worker.set_interval(interval_ms)
            logger.info(f"Scan interval updated to {interval_ms}ms")
    
    def connect_signals(self, 
                        on_scan_complete=None,
                        on_scan_error=None,
                        on_channel_read=None,
                        on_scan_started=None,
                        on_scan_stopped=None) -> None:
        """
        Connect manager signals to callback functions.
        
        Args:
            on_scan_complete: Callback for scan_complete signal (receives dict)
            on_scan_error: Callback for scan_error signal (receives str)
            on_channel_read: Callback for channel_read signal (receives int, float)
            on_scan_started: Callback for scan_started signal
            on_scan_stopped: Callback for scan_stopped signal
        """
        if on_scan_complete:
            self.scan_complete.connect(on_scan_complete)
        if on_scan_error:
            self.scan_error.connect(on_scan_error)
        if on_channel_read:
            self.channel_read.connect(on_channel_read)
        if on_scan_started:
            self.scan_started.connect(on_scan_started)
        if on_scan_stopped:
            self.scan_stopped.connect(on_scan_stopped)
    
    def _on_worker_scan_stopped(self) -> None:
        """Handle worker scan stopped signal - quit the thread and emit manager signal."""
        logger.debug("Worker scan stopped, quitting thread")
        if self._thread:
            self._thread.quit()
        # Emit manager's scan_stopped signal for external handlers
        self.scan_stopped.emit()
    
    def _on_thread_finished(self) -> None:
        """Handle thread finished signal."""
        logger.debug("Scan thread finished")
        self._scanning = False
    
    def _cleanup(self) -> None:
        """Clean up thread and worker resources."""
        self._scanning = False
        
        if self._thread:
            if self._thread.isRunning():
                self._thread.quit()
                self._thread.wait(1000)
            self._thread.deleteLater()
            self._thread = None
        
        if self._worker:
            self._worker.deleteLater()
            self._worker = None
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
        self._cleanup()
