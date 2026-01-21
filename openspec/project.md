# Project Context

## Purpose
The SDM4055A_Controller is a Python-based GUI application for communicating with and reading measurements from Siglent SDM4055A-SC 5½ digit digital multimeter via USB connection using VISA protocol.

### Initial Phase (MVP)
The first version focuses on a simple test application to:
- Establish USB connection to SDM4055A-SC multimeter
- Read measurement data from one channel (connected to standard probes)
- Display measured value on a modern digital indicator
- Verify basic communication and data retrieval functionality

### Future Phases
- Multi-channel monitoring using SC1016 scanner card (16 channels: 12 multi-purpose + 4 current)
- Historical data logging and analysis
- Advanced measurement parameters (all supported functions)
- Configuration and calibration features
- Data export capabilities
- Remote monitoring via VNC/web server integration

## Tech Stack
- **Language**: Python 3.10+
- **GUI Framework**: `PySide6` (Qt for Python)
- **Device Communication**: `PyVISA` (Virtual Instrument Software Architecture)
- **Theme/Styling**: `qt-material` (Modern dark theme engine for Qt)
- **Packaging**: `PyInstaller` (Standalone Windows Executable)
- **Dependency Management**: `uv` (Modern, fast Python package manager)

### Key Libraries & Versions
- `PySide6>=6.0.0`: Core UI library
- `qt-material>=2.14`: Theming
- `pyvisa>=1.14.0`: Industry standard instrument control
- `pyinstaller>=6.0.0`: Build tool

## Project Conventions

### Code Style
- **PEP 8**: Follow Python Enhancement Proposal 8 style guide
- **Naming Conventions**:
  - Variables and functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private members: `_leading_underscore`
- **Line Length**: Maximum 100 characters (soft limit 120)
- **Imports**: Group imports in order: standard library, third-party, local modules
- **Type Hints**: Use type hints for function signatures where appropriate
- **Docstrings**: Google-style docstrings for classes and public functions

### Architecture Patterns

#### Application Structure
- **Entry Point**: `main.py` initializes `QApplication`, applies theme, and launches `MainWindow`
- **Modular Design**:
  - `gui/`: Contains all UI-related code (`window.py`, `widgets.py`)
  - `hardware/`: Abstraction layer for device communication (`visa_interface.py` vs `simulator.py`)

#### Concurrency & Timing
- **Data Acquisition**: Utilizes `QTimer` in the main UI thread for periodic polling (set to 500ms)
- **Rationale**: For simple multimeter reading (approx. 2-5Hz), a timer is sufficient and avoids the complexity of `QThread` synchronization. If higher frequency is needed, a dedicated `QThread` with `Signal/Slot` mechanism should be adopted

#### Hardware Abstraction
- **Simulator Pattern**: To facilitate development without physical hardware, a `VisaSimulator` class mocks the API of the real `VisaInterface`
- **Switching**: The active driver is currently hardcoded in `MainWindow.toggle_connection` but designed to be hot-swapped by uncommenting the relevant lines (or via configuration injection in future)

#### GUI Components
- **Custom Widgets**: `DigitalIndicator` (in `gui/widgets.py`) encapsulates a "Card" style display with shadow effects, implementing a reusable component for each channel
- **Theming**: `qt-material` is applied globally in `main.py` using `apply_stylesheet(app, theme='dark_teal.xml')`

### Testing Strategy
- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test VISA communication with mock devices or actual hardware
- **GUI Tests**: Test UI components and user interactions
- **Test Framework**: `pytest` with `pytest-qt` for GUI testing and `pytest-mock` for mocking
- **Coverage**: Aim for >80% code coverage for core functionality
- **Hardware Testing**: Document procedures for testing with actual SDM4055A-SC device

### Git Workflow
- **Branching Strategy**: Feature branch workflow
  - `main`: Production-ready code
  - `develop`: Integration branch for features
  - `feature/*`: Feature branches
- **Commit Messages**: Conventional Commits format
  - `feat:`: New features
  - `fix:`: Bug fixes
  - `docs:`: Documentation changes
  - `refactor:`: Code refactoring
  - `test:`: Test additions/modifications
  - `style:`: Code style changes (formatting, etc.)
- **Pull Requests**: Required for merging into `develop` or `main`

## Domain Context

### Device Overview
The **Siglent SDM4055A-SC** is a 5½ digit (220,000 count) high-precision digital multimeter with outstanding measurement accuracy and a 5-inch TFT touchscreen display. It is designed for high-precision, multifunctional, and automatic measurement needs in research laboratories, development laboratories, repair and maintenance, calibration laboratories, and automatic production testing.

### Key Specifications
- **Display Resolution**: Real 5½ digit (220,000 count) readings
- **DCV Basic Accuracy**: 150 ppm
- **Max Reading Rate**: 4,800 rdgs/s (configurable: 5 rdgs/s to 4.8k rdgs/s)
- **Memory**: 512 MB RAM (up to 2M readings for caching), 256 MB NAND Flash for file storage
- **Display**: 5-inch TFT-LCD touchscreen (800×480 resolution)
- **Communication**: SCPI-compliant remote control commands
- **Scanner Card**: SC1016 (12 multi-purpose + 4 current channels) - SDM4055A-SC model only

### Supported Measurement Functions
1. **DC Voltage (DCV)**: 200 mV ~ 1000 V
2. **AC Voltage (ACV)**: 200 mV ~ 750 V, 20 Hz ~ 100 kHz (True-RMS)
3. **DC Current (DCI)**: 200 μA ~ 10 A
4. **AC Current (ACI)**: 20 mA ~ 10 A, 20 Hz ~ 10 kHz (True-RMS)
5. **2/4-Wire Resistance**: 200 Ω ~ 100 MΩ
6. **Capacitance**: 2 nF ~ 10 mF
7. **Frequency / Period**: 20 Hz ~ 1 MHz
8. **Temperature**: RTD (Pt100), Thermocouple (B, E, J, K, N, R, S, T types)
9. **Continuity Test**: With buzzer
10. **Diode Test**: 4 V max

### Advanced Features
- **Trigger Modes**: Auto trigger, single trigger, external trigger, level trigger
- **Display Modes**: Numerical, bar meter, trend chart, histogram
- **Math Functions**: Max, Min, Average, Standard Deviation, dBm/dB, Limits
- **Data Log**: 0.1 s ~ 3600 s interval, up to 2M points to memory, 360M points to files
- **Automatic Current Switching**: 10 A high current and 3 A low current modes (up to 30 A with external shunt)
- **Dual Display**: Simultaneous display of two measurements
- **Probe Hold**: Hold measurement values
- **Measurement Speed Modes**: Fast, Medium, Slow

### Communication Interfaces
- **USB Device**: Primary connection for PC control
- **USB Host**: For external storage devices
- **LAN**: Ethernet connectivity
- **GPIB**: Optional (requires USB-GPIB adapter)
- **Remote Access**: VNC and web server support

### Initial Phase Scope
For MVP, we focus on:
- **Single Channel**: Reading from one measurement channel (standard probe connection to front panel)
- **Basic Measurement**: Primary measurement type (typically DC voltage or current based on probe configuration)
- **Connection Test**: Verify USB/VISA communication establishment
- **Real-time Display**: Show current measurement value with modern UI

The device communicates via USB using VISA protocol, which is an industry standard for instrument control. VISA provides a unified API for communicating with various test and measurement instruments, regardless of underlying bus (USB, GPIB, Ethernet, Serial). The application uses PyVISA, a Python wrapper around VISA library, to communicate with device. The SDM4055A-SC supports SCPI (Standard Commands for Programmable Instruments) commands for remote control.

## Important Constraints
- **USB Port Availability**: Requires exclusive access to USB port during operation
- **VISA Driver**: Must have appropriate VISA runtime and device drivers installed (e.g., NI-VISA, Keysight VISA)
- **Timing Constraints**: Polling interval (default 500ms) balances responsiveness with system resources; device supports up to 4,800 rdgs/s
- **GUI Thread**: Data acquisition runs on main UI thread via QTimer; avoid blocking operations
- **Hardware Compatibility**: Must work with SDM4055A-SC device specifications and VISA resource strings
- **Error Recovery**: Must handle communication failures gracefully (timeouts, disconnections)
- **Cross-Platform**: Application should work on Windows (primary target), Linux, and macOS with appropriate VISA drivers
- **Packaging**: PyInstaller must include hidden imports (`qt_material`) and data files (`gui`, `hardware` directories)
- **Scanner Card**: When using SC1016 scanner card, front panel inputs must be floating to avoid damage

## External Dependencies
- **Hardware**: Siglent SDM4055A-SC 5½ digit digital multimeter with USB interface
- **VISA Runtime**: NI-VISA, Keysight VISA, or compatible VISA implementation
- **USB Drivers**: Device-specific USB drivers if required by meter
- **Python Packages**:
  - `PySide6>=6.0.0`: Qt for Python GUI framework
  - `qt-material>=2.14`: Modern dark theme for Qt applications
  - `pyvisa>=1.14.0`: VISA protocol implementation for Python
  - `pyinstaller>=6.0.0`: Application packaging tool
  - `pytest>=7.0` (dev): Testing framework
  - `pytest-qt>=4.0` (dev): Qt testing support
  - `pytest-mock>=3.0` (dev): Mocking support
- **System Requirements**: Python 3.10+, VISA runtime, available USB port, Windows (primary) or Linux/macOS with appropriate drivers
- **Build System**: `uv` package manager for dependency management and environment setup
- **Build Script**: `build_exe.bat` automates PyInstaller build with necessary configurations

## Build System Details
- **Environment**: Managed via `uv` for fast, modern Python package management
- **Build Script**: `build_exe.bat` automates `PyInstaller` command with:
  - Hidden imports: `qt_material` (required for theming)
  - Data file inclusion: `gui`, `hardware` directories
  - Standalone Windows executable output

## Recent Changes (2026-01-21)

### New Features
1. **Serial Number Input Field**
   - Added serial number input field in the "Scan Control" section of the main window
   - Implemented real-time validation using regex pattern `^PSN\d{9}$` (PSN followed by exactly 9 digits)
   - Visual feedback system:
     - White text color for valid serial number format
     - Red text color for invalid serial number format
     - Default color for empty input
   - Added placeholder text "PSN123456789" to guide users
   - Hidden unused "Start Scan" and "Stop Scan" buttons (set visible to False)
   - "Single Scan" button remains functional and visible

### Modified Files
- **gui/window.py**:
  - Added `re` module import for regex validation
  - Added `QLineEdit` import from PySide6.QtWidgets
  - Created `serial_number_input` QLineEdit widget in Scan Control section
  - Created `lbl_serial_number` QLabel for field identification
  - Implemented `_on_serial_number_changed()` method for validation
  - Connected `textChanged` signal to validation handler
  - Set `setVisible(False)` on `btn_start_scan` and `btn_stop_scan`

### Testing
- **test_serial_number_validation.py** (NEW): Comprehensive test suite for serial number validation
  - 16 test cases covering valid/invalid formats and edge cases
  - All tests passed successfully

### Archived Proposals
- **add-serial-number-input** → archived in `openspec/changes/archive/2026-01-21-add-serial-number-input/`

## Recent Changes (2026-01-19)

### New Features
1. **Unit Display and Overload Detection**
    - Added `ScanDataResult` dataclass to capture unit information from multimeter responses
    - Implemented unit parsing from SCPI responses (e.g., "VDC" → "V", "ADC" → "A")
    - Added overload detection with two methods:
      - String detection: checks for "overload" in response (case-insensitive)
      - Value threshold: detects values > 1e35 (multimeter's overload indicator)
    - Updated signal types to pass `ScanDataResult` objects instead of `float`
    - Enhanced GUI to display overload messages (e.g., "overloadDC") in red color
    - Added unit display support for AUTO range (uses unit from multimeter response)
    - Implemented backward compatibility for `float` values

### Modified Files
- **hardware/visa_interface.py**:
  - Added `ScanDataResult` dataclass with value, unit, full_unit, and range_info fields
  - Updated `get_scan_data()` to return `ScanDataResult` objects
  - Implemented unit parsing logic with comprehensive unit mapping
  - Added overload detection with proper message construction
  - Updated `read_all_channels()` return type to `Dict[int, Optional[ScanDataResult]]`
  - Updated `_read_channels_sequentially()` return type to `Dict[int, Optional[ScanDataResult]]`

- **hardware/async_worker.py**:
  - Added `ScanDataResult` import
  - Updated `channel_read` signal type from `Signal(int, float)` to `Signal(int, object)`

- **gui/window.py**:
  - Added `ScanDataResult` import
  - Updated `_on_scan_complete()` to handle `ScanDataResult` objects with overload detection
  - Updated `_on_single_scan_complete()` to handle `ScanDataResult` objects with overload detection
  - Updated `_on_channel_read()` to handle `ScanDataResult` objects with backward compatibility

- **gui/widgets.py**:
  - Updated `set_value()` method to accept and use unit parameter
  - Added comments explaining AUTO range behavior (uses unit from multimeter response)

### Documentation
- **doc/UNIT_AND_OVERLOAD_FIX.md** (NEW): Comprehensive documentation of unit display and overload detection implementation

### Archived Proposals
- **add-dynamic-unit-display** → archived in `openspec/changes/archive/2026-01-19-unit-and-overload-display/`
- **add-range-based-unit-display** → archived in `openspec/changes/archive/2026-01-19-unit-and-overload-display/`
- **2026-01-19-compact-value-display** → archived in `openspec/changes/archive/2026-01-19-compact-value-display/`

## Recent Changes (2026-01-14)

### New Features
1. **Channel Configuration File Loading**
   - Added CSV-based configuration file support for channel settings
   - Created `config/config_loader.py` module with full validation logic
   - Added "Load Config" button to Scan Control section in main window
   - Configuration file format includes:
     - Channel number (1-16)
     - Measurement type (VOLT:DC, VOLT:AC, RES, FRES, CAP, FREQ, DIOD, CONT, TEMP:RTD, TEMP:THER, CURR:DC, CURR:AC)
     - Range (AUTO or specific value)
     - Lower threshold (optional)
     - Upper threshold (optional)
   - Supports partial channel configuration (configure only channels you need)
   - Supports comment lines in CSV files (lines starting with #)
   - Displays loaded configuration file name in UI
   - Comprehensive validation with detailed error messages:
     - Channel number validation (1-16)
     - Measurement type validation per channel (channels 1-12: voltage/resistance, channels 13-16: current)
     - Threshold value validation (numeric, lower < upper)
   - Created `sample_config.csv` with example configurations and documentation

2. **Threshold-Based Color Coding and Display**
   - Added threshold support to `ChannelIndicator` widget
   - Implemented automatic color coding based on thresholds:
     - GREEN: value within configured thresholds
     - RED: value outside configured thresholds
   - Added threshold display label showing configured thresholds:
     - Shows lower threshold as "≥value"
     - Shows upper threshold as "≤value"
     - Displays both thresholds separated by " | "
     - Hidden when no thresholds configured
   - Increased measurement value font size from 28pt to 36pt for better readability
   - Thresholds can be configured via CSV file or programmatically
   - Supports lower-only, upper-only, or both thresholds
   - Thresholds can be cleared to disable color coding
   - Color updates automatically when measurement values are updated

### Modified Files
- **config/config_loader.py** (NEW): Configuration parser with validation
- **config/__init__.py** (NEW): Package initialization
- **gui/window.py**: Added config loading UI and logic
- **gui/widgets.py**: Added threshold support to ChannelIndicator
- **sample_config.csv** (NEW): Example configuration file

## Recent Changes (2026-01-13)

### Bug Fixes
1. **hardware/simulator.py** - Fixed missing `List` import from typing module
   - Added `List` to imports to resolve NameError

2. **gui/window.py** - Fixed narrow device selection dropdown
   - Increased minimum width to 400px
   - Set minimum contents length to 50 characters
   - Ensures full device names are visible

3. **gui/window.py** - Fixed incorrect method call
   - Changed `indicator.reset()` to `indicator.reset_status()`
   - Corrects AttributeError when disconnecting

4. **hardware/async_worker.py** - Fixed RuntimeError during thread cleanup
   - Added try-catch for RuntimeError when thread is already deleted
   - Prevents crashes during application shutdown

### New Features
1. **Virtual Multimeter Simulator Integration**
   - Added simulator as first option in device selection dropdown
   - Allows testing without physical hardware
   - Supports all 16 channels with realistic measurements:
     - Channels 1-12: DC voltage ~5V
     - Channels 13-16: DC current ~0.5A
   - Fully compatible with existing AsyncScanManager
   - Auto-selected on application startup

### Discovered VISA Devices
The following physical devices were detected on the system:
- **ASRL3::INSTR (COM3)**: USB-SERIAL CH340 adapter (VID_1A86&PID_7523)
- **ASRL4::INSTR (COM4)**: Bluetooth Serial Port
- **ASRL5::INSTR (COM5)**: Bluetooth Serial Port

### Running the Application
```bash
# Using venv_new virtual environment
venv_new\Scripts\python.exe main.py

# Or after activating the environment
venv_new\Scripts\activate
python main.py
```
