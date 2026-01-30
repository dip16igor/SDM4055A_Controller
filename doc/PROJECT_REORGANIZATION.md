# Project Reorganization - 2026-01-30

## Overview

The project structure has been reorganized to improve maintainability and clarity. All files are now properly categorized into logical directories.

## New Directory Structure

### 📁 Root Directory (Clean)
Only essential files remain in the root:
- `main.py` - Application entry point
- `version.py` - Application version
- `requirements.txt` - Python dependencies
- `README.md` - Main documentation
- `.gitignore` - Git ignore rules

### 📁 build/
Build scripts and configuration files:
- `build_app.bat` - Main build script (recommended)
- `build_exe.bat` - Alternative build script
- `*.spec` - PyInstaller spec files

**Usage:**
```cmd
build\build_app.bat
```

### 📁 scripts/
Helper scripts and test files:
- `create_icon.py` - Icon generation script
- `test_*.py` - Test and development scripts

**Usage:**
```cmd
python scripts\create_icon.py
```

### 📁 assets/icons/
Application icon files:
- `app_icon.ico` - Main application icon
- `app_icon_*.png` - Icon previews in various sizes

### 📁 examples/
Example configuration files:
- CSV files for various board configurations
- Test data files

### 📁 doc/
Documentation files:
- `BUILD_README.md` - Build instructions
- `BUILD_SUMMARY.md` - Build summary
- `RANGE_*.md` - Range implementation documentation
- Other technical documentation

### 📁 gui/
GUI components (unchanged):
- `window.py` - Main application window
- `widgets.py` - Custom widgets
- `theme_manager.py` - Theme management

### 📁 hardware/
Hardware abstraction layer (unchanged):
- `visa_interface.py` - VISA communication
- `simulator.py` - Device simulator
- `async_worker.py` - Async operations
- `simple_scanner.py` - Simple scanner

### 📁 config/
Configuration management (unchanged):
- `config_loader.py` - Configuration file loader

## Migration Guide

### For Users

If you have existing workflows, update your commands:

**Old command:**
```cmd
build_exe.bat
```

**New command:**
```cmd
build\build_app.bat
```

**Old icon path:**
```
app_icon.ico
```

**New icon path:**
```
assets\icons\app_icon.ico
```

### For Developers

**Import paths remain unchanged** - all Python modules are still accessible:
- `from gui.window import MainWindow`
- `from hardware.visa_interface import VisaInterface`
- `from config.config_loader import ConfigLoader`

**Test scripts are now in scripts/ directory:**
```cmd
python scripts\test_icon.py
```

## Benefits

1. **Cleaner Root Directory** - Only essential files in the root
2. **Better Organization** - Files grouped by purpose
3. **Easier Navigation** - Clear separation of concerns
4. **Professional Structure** - Follows Python project best practices
5. **Maintainability** - Easier to find and update files

## Build Script Updates

The build scripts have been updated to use the new paths:

- Icons are now in `assets\icons\`
- Helper scripts are in `scripts\`
- Build scripts are in `build\`

All functionality remains the same - only paths have changed.

## Git Considerations

The `.gitignore` file has been updated to document the new structure:
- `scripts/` - Helper scripts (kept)
- `assets/icons/` - Icon files (kept)
- `examples/` - Example files (kept)
- `doc/` - Documentation (kept)

## Removed Files

The following junk files have been removed:
- `-p/` directory (empty artifact)
- `test_output.txt` (temporary file)
- `3.1.0` (unknown file)

## Summary

This reorganization improves the project structure without breaking any functionality. All paths have been updated in the build scripts, and the project is now better organized for long-term maintenance.
