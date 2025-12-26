# AI Project Context: USB VISA Multimeter App

This document outlines the technical stack, architectural decisions, and libraries used in this project. It is intended to provide context for AI assistants working on this codebase.

## 1. Technology Stack

- **Language**: Python 3.10+
- **GUI Framework**: `PySide6` (Qt for Python)
- **Device Communication**: `PyVISA` (Virtual Instrument Software Architecture)
- **Theme/Styling**: `qt-material` (Modern dark theme engine for Qt)
- **Packaging**: `PyInstaller` (Standalone Windows Executable)
- **Dependency Management**: `uv` (Modern, fast Python package manager)

## 2. Architectural Approaches

### Application Structure
- **Entry Point**: `main.py` initializes the `QApplication`, applies the theme, and launches the `MainWindow`.
- **Modular Design**:
    - `gui/`: Contains all UI-related code (`window.py`, `widgets.py`).
    - `hardware/`: Abstraction layer for device communication (`visa_interface.py` vs `simulator.py`).

### Concurrency & Timing
- **Data Acquisition**: Utilizes `QTimer` in the main UI thread for periodic polling (set to 500ms).
- **Rationale**: For simple multimeter reading (approx. 2-5Hz), a timer is sufficient and avoids the complexity of `QThread` synchronization. If higher frequency is needed, a dedicated `QThread` with `Signal/Slot` mechanism should be adopted.

### Hardware Abstraction
- **Simulator Pattern**: To facilitate development without physical hardware, a `VisaSimulator` class mocks the API of the real `VisaInterface`.
- **Switching**: The active driver is currently hardcoded in `MainWindow.toggle_connection` but designed to be hot-swapped by uncommenting the relevant lines (or via configuration injection in future).

### GUI Components
- **Custom Widgets**: `DigitalIndicator` (in `gui/widgets.py`) encapsulates a "Card" style display with shadow effects, implementing a reusable component for each channel.
- **Theming**: `qt-material` is applied globally in `main.py` using `apply_stylesheet(app, theme='dark_teal.xml')`.

## 3. Key Libraries & Versions (from requirements.txt)
- `PySide6>=6.0.0`: Core UI library.
- `qt-material>=2.14`: Theming.
- `pyvisa>=1.14.0`: Industry standard instrument control.
- `pyinstaller>=6.0.0`: Build tool.

## 4. Build System
- **Environment**: Managed via `uv`.
- **Build Script**: `build_exe.bat` automates the `PyInstaller` command with necessary hidden imports (`qt_material`) and data file inclusion (`gui`, `hardware`).
