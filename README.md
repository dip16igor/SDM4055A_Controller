# SDM4055A-SC Multimeter Controller

A modern GUI application for monitoring the Siglent SDM4055A-SC 5½ digit digital multimeter via USB using VISA protocol.

## Features

- **Real-time Measurement Display**: Modern card-style digital indicator with shadow effects
- **USB/VISA Communication**: Connects to SDM4055A-SC via USB using industry-standard VISA protocol
- **Hardware Abstraction**: Supports both real device and simulator modes for development
- **Modern Dark Theme**: Built with PySide6 and qt-material for a professional appearance
- **Periodic Polling**: Automatic data acquisition at 500ms intervals
- **Error Handling**: Graceful handling of communication failures and disconnections
- **Standalone Executable**: Packaged as Windows executable for easy deployment

## Requirements

### Hardware
- Siglent SDM4055A-SC 5½ digit digital multimeter
- USB cable for device connection

### Software
- Python 3.10 or higher
- VISA Runtime (NI-VISA, Keysight VISA, or compatible)
- Device-specific USB drivers (if required)

## Installation

### 1. Install VISA Runtime

Download and install one of the following VISA runtimes:

- **NI-VISA**: https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html
- **Keysight VISA**: https://www.keysight.com/en/pn-2903822-io-libraries-suite

### 2. Clone or Download the Project

```bash
git clone <repository-url>
cd SDM4055A_Controller
```

### 3. Create Virtual Environment (Recommended)

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

### 4. Install Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Using uv (recommended for faster installation):
```bash
uv pip install -r requirements.txt
```

## Usage

### Running the Application

#### Simulator Mode (Default)
Run without physical hardware for testing:
```bash
python main.py
```

The application will start in simulator mode, displaying mock measurement values.

#### Real Device Mode

To connect to the actual SDM4055A-SC device:

1. Connect the multimeter to your computer via USB
2. Open `gui/window.py` and modify line 18:
   ```python
   self._use_simulator = False  # Set to False to use real device
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. Click the "Connect" button to establish connection
5. Measurement values will be displayed and updated every 500ms

### Building Standalone Executable

To create a standalone Windows executable:

**Quick build (recommended):**
```bash
build\build_app.bat
```

**Or alternative build script:**
```bash
build\build_exe.bat
```

The executable will be created in the `dist/` directory as `SDM4055A_Controller.exe`.

**Note**: It's recommended to use a virtual environment for building:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
build\build_app.bat
```

## Project Structure

```
SDM4055A_Controller/
├── main.py                 # Application entry point
├── version.py              # Application version
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
│
├── build/                 # Build scripts and artifacts
│   ├── build_app.bat      # Main build script (recommended)
│   ├── build_exe.bat      # Alternative build script
│   └── *.spec             # PyInstaller spec files
│
├── scripts/               # Helper and test scripts
│   ├── create_icon.py     # Icon generation script
│   └── test_*.py          # Test and development scripts
│
├── assets/                # Application assets
│   └── icons/             # Icon files
│       ├── app_icon.ico   # Main application icon
│       └── app_icon_*.png # Icon previews
│
├── examples/              # Example configuration files
│   ├── B1ComputerBoard.csv
│   ├── B1ControlExtensionBoardv232.csv
│   ├── Boreas_2v1.csv
│   └── test1.csv
│
├── doc/                   # Documentation
│   ├── BUILD_README.md
│   ├── BUILD_SUMMARY.md
│   ├── RANGE_*.md         # Range implementation docs
│   └── *.md              # Other documentation
│
├── gui/                   # GUI components
│   ├── __init__.py
│   ├── window.py          # Main application window
│   ├── widgets.py         # Custom widgets (DigitalIndicator)
│   └── theme_manager.py   # Theme management
│
├── hardware/              # Hardware abstraction layer
│   ├── __init__.py
│   ├── visa_interface.py  # VISA communication interface
│   ├── simulator.py       # Mock device simulator
│   ├── async_worker.py    # Async scanning operations
│   └── simple_scanner.py  # Simple scanner implementation
│
├── config/                # Configuration management
│   ├── __init__.py
│   └── config_loader.py   # Configuration file loader
│
└── openspec/              # OpenSpec specifications
    ├── project.md         # Project context and conventions
    ├── changes/           # Change proposals
    └── specs/            # Capability specifications
```

## Troubleshooting

### Device Not Found

**Problem**: "No VISA resources found" or connection fails

**Solutions**:
1. Ensure VISA runtime is installed correctly
2. Check USB cable connection
3. Verify device is powered on
4. Run NI MAX (for NI-VISA) to verify device is detected
5. Try different USB port

### Import Errors

**Problem**: `ModuleNotFoundError` for PySide6, qt-material, or pyvisa

**Solution**:
```bash
pip install -r requirements.txt
```

### Theme Not Applied

**Problem**: Application looks different than expected

**Solution**: Ensure qt-material is installed:
```bash
pip install qt-material>=2.14
```

### Polling Issues

**Problem**: Measurements not updating or showing errors

**Solutions**:
1. Check device is still connected
2. Verify measurement function is supported (default: DC Voltage)
3. Check VISA timeout settings in `hardware/visa_interface.py`
4. Review application logs for error messages

## Development

### Running Tests

```bash
pytest
```

### Code Style

The project follows PEP 8 conventions. Run linting:
```bash
flake8 .
```

## Technical Details

### Supported Measurements (MVP)
- DC Voltage (DCV): 200 mV ~ 1000 V
- Future versions will support: ACV, DCI, ACI, Resistance, Capacitance, Frequency, Temperature

### Communication Protocol
- **Protocol**: VISA (Virtual Instrument Software Architecture)
- **Interface**: USB Device
- **Commands**: SCPI-compliant commands

### GUI Framework
- **Library**: PySide6 (Qt for Python)
- **Theme**: qt-material (dark_teal)
- **Architecture**: QTimer-based polling in main UI thread

## License

[Add your license information here]

## Recent Changes

### 2026-01-28 - Animated Progress Indicator for Single Scan
- **Added**: Animated progress indicator widget (`ChannelProgressIndicator`) to replace text status label
- **Features**:
  - Spinning animation (| / - \) during scanning
  - Checkmark (✓) displayed briefly after scan completes
  - Resets to X icon (◌) after 500ms
  - Theme-aware styling for both dark and light modes
- **Removed**: All text labels near Scan button
- **Fixed**: GUI freezing issue during single scan operations
  - Implemented `SingleScanWorker` class to perform single scan in background thread
  - Added proper thread lifecycle management to prevent "QThread: Destroyed while thread is still running" errors
  - Status bar now shows "Ready" after single scan completion
- **Files Modified**:
  - `gui/widgets.py`: Added `ChannelProgressIndicator` class, removed text labels
  - `hardware/async_worker.py`: Added `SingleScanWorker` class, updated `AsyncScanManager.start_single_scan()` method
  - `gui/window.py`: Integrated progress indicator, added temporary manager reference management

## Support

For issues, questions, or contributions:
- Open an issue on the project repository
- Refer to Siglent SDM4055A-SC documentation: https://int.siglent.com/products-document/sdm4055a/

## Acknowledgments

- Siglent Technologies for the SDM4055A-SC multimeter
- Qt Project for the PySide6 framework
- qt-material for the modern theme engine
