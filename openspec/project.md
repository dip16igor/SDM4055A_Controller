# Project Context

## Purpose
The SDM4055A_Controller is a Python-based GUI application for communicating with and reading measurements from the SDM4055A power/energy meter device via USB connection using the VISA protocol.

### Initial Phase (MVP)
The first version focuses on a simple test application to:
- Establish USB connection to the SDM4055A multimeter
- Read measurement data from one channel (connected to standard probes)
- Display the measured value on a modern digital indicator
- Verify basic communication and data retrieval functionality

### Future Phases
- Multi-channel monitoring
- Historical data logging
- Advanced measurement parameters (power, energy, frequency)
- Configuration and calibration features
- Data export capabilities

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
- **Entry Point**: `main.py` initializes the `QApplication`, applies the theme, and launches the `MainWindow`
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
- **Hardware Testing**: Document procedures for testing with actual SDM4055A device

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
The SDM4055A is a digital power meter that measures electrical parameters including:
- Voltage (V): AC voltage measurements
- Current (A): AC current measurements
- Power (W, kW, VA, VAR): Active, reactive, and apparent power
- Energy (kWh, kVARh): Accumulated energy consumption
- Power Factor (PF): Ratio of real to apparent power
- Frequency (Hz): Line frequency

### Initial Phase Scope
For the MVP, we focus on:
- **Single Channel**: Reading from one measurement channel (standard probe connection)
- **Basic Measurement**: Primary measurement type (typically voltage or current based on probe configuration)
- **Connection Test**: Verify USB/VISA communication establishment
- **Real-time Display**: Show current measurement value with modern UI

The device communicates via USB using the VISA protocol, which is an industry standard for instrument control. VISA provides a unified API for communicating with various test and measurement instruments, regardless of the underlying bus (USB, GPIB, Ethernet, Serial). The application uses PyVISA, a Python wrapper around the VISA library, to communicate with the device.

## Important Constraints
- **USB Port Availability**: Requires exclusive access to USB port during operation
- **VISA Driver**: Must have appropriate VISA runtime and device drivers installed (e.g., NI-VISA, Keysight VISA)
- **Timing Constraints**: Polling interval (default 500ms) balances responsiveness with system resources
- **GUI Thread**: Data acquisition runs on main UI thread via QTimer; avoid blocking operations
- **Hardware Compatibility**: Must work with SDM4055A device specifications and VISA resource strings
- **Error Recovery**: Must handle communication failures gracefully (timeouts, disconnections)
- **Cross-Platform**: Application should work on Windows (primary target), Linux, and macOS with appropriate VISA drivers
- **Packaging**: PyInstaller must include hidden imports (`qt_material`) and data files (`gui`, `hardware` directories)

## External Dependencies
- **Hardware**: SDM4055A power/energy meter device with USB interface
- **VISA Runtime**: NI-VISA, Keysight VISA, or compatible VISA implementation
- **USB Drivers**: Device-specific USB drivers if required by the meter
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
- **Build Script**: `build_exe.bat` automates the `PyInstaller` command with:
  - Hidden imports: `qt_material` (required for theming)
  - Data file inclusion: `gui`, `hardware` directories
  - Standalone Windows executable output
