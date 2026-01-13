# Change: Add Asynchronous Scanning for Non-Blocking UI

**Status:** Completed
**Created:** 2025-12-26
**Completed:** 2025-12-26

## Why
The current implementation performs device I/O operations (reading measurements from all channels) in the GUI thread using QTimer. When the device communication is slow or encounters delays, the entire interface freezes and becomes unresponsive. This creates a poor user experience as users cannot interact with the UI during scanning operations.

## What Changes
- Move device I/O operations to background threads using QThread
- Implement asynchronous communication pattern for device reads
- Add progress indicators to show scanning activity
- Ensure UI remains responsive during all device operations
- Add cancellation support for ongoing scans
- Implement proper thread-safe communication between worker threads and GUI

## Impact
- Affected specs: multimeter-controller
- Affected code: gui/window.py, hardware/visa_interface.py, hardware/simulator.py
- New files: hardware/async_worker.py

## Implementation Summary

### Files Created
1. **`hardware/async_worker.py`**
   - `ScanWorker` class - QThread-based worker for background scanning
   - `AsyncScanManager` class - Manager for worker lifecycle and signal connections

2. **`openspec/changes/add-async-scanning/proposal.md`** - This proposal document

3. **`openspec/changes/add-async-scanning/specs/multimeter-controller/spec.md`** - Detailed requirements

4. **`openspec/changes/add-async-scanning/tasks.md`** - Implementation checklist

### Files Modified
1. **`hardware/__init__.py`**
   - Added exports: `ScanWorker`, `AsyncScanManager`

2. **`hardware/visa_interface.py`**
   - Added thread safety with QMutex
   - Wrapped critical methods with QMutexLocker

3. **`hardware/simulator.py`**
   - Added thread safety with QMutex
   - Wrapped critical methods with QMutexLocker

4. **`gui/window.py`**
   - Replaced QTimer-based scanning with AsyncScanManager
   - Added visual progress indicators
   - Connected all worker signals to UI update methods

## Testing Results
The implementation has been tested and verified:

1. ✅ UI remains responsive during scanning
2. ✅ START button becomes disabled when scanning starts
3. ✅ STOP button becomes enabled when scanning starts
4. ✅ Application does not close when pressing START during scanning
5. ✅ Scanning status indicator shows "Scanning" during active scans
6. ✅ Activity indicator animates during scanning
7. ✅ Clean shutdown when closing the window
