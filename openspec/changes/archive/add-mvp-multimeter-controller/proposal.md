# Change: Add MVP Multimeter Controller Application

## Why
Create a minimal viable product to verify USB communication with the Siglent SDM4055A-SC multimeter and display measurements on a modern GUI. This establishes the foundation for future multi-channel monitoring and advanced features.

## What Changes
- Create Python GUI application using PySide6 with modern dark theme
- Implement VISA-based USB communication with SDM4055A-SC device
- Add hardware abstraction layer supporting real device and simulator modes
- Create custom digital indicator widget for measurement display
- Implement periodic data polling (500ms) using QTimer
- Add connection/disconnection functionality
- Include error handling for communication failures

## Impact
- Affected specs: New capability `multimeter-controller`
- Affected code: New project structure with `main.py`, `gui/`, and `hardware/` directories
- Dependencies: PySide6, qt-material, pyvisa, pyinstaller
