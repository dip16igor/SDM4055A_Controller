# Building SDM4055A-SC Controller Executable

## Icon Issue Resolution

The application was showing a default Python icon in the Windows taskbar instead of the custom multimeter icon. This occurred because:

1. **Runtime icon vs. Embedded icon**: The application was setting icons programmatically at runtime using `QApplication.setWindowIcon()`, but Windows taskbar requires the icon to be **embedded in the executable file itself**.

2. **PyInstaller requirement**: When building with PyInstaller, the `--icon` parameter is needed to embed the icon into the executable, which Windows then uses for the taskbar.

## Build Instructions

### Quick Build (Recommended)

Simply run the comprehensive build script:

```cmd
build_app.bat
```

This script will:
1. Generate the application icon file (`app_icon.ico`)
2. Build the executable with the icon embedded
3. Place the output in `dist/SDM4055A_Controller.exe`

### Manual Build Steps

If you prefer to build manually:

#### Step 1: Generate Icon

```cmd
python create_icon.py
```

This creates:
- `app_icon.ico` - Main icon file for the executable
- `app_icon_16x16.png` through `app_icon_256x256.png` - Preview images

#### Step 2: Build Executable

```cmd
python -m PyInstaller --onefile ^
    --windowed ^
    --name SDM4055A_Controller ^
    --icon app_icon.ico ^
    --hidden-import qt_material ^
    --hidden-import config ^
    --hidden-import config.config_loader ^
    --add-data "gui;gui" ^
    --add-data "hardware;hardware" ^
    --add-data "config;config" ^
    main.py
```

### Or use the original build script (updated):

```cmd
build_exe.bat
```

## Output

After building, you'll find:
- **Executable**: `dist/SDM4055A_Controller.exe`
- **Icon file**: `app_icon.ico` (in project root)

## Testing

Run the executable:
```cmd
dist\SDM4055A_Controller.exe
```

The application icon should now appear correctly in:
- ✅ Windows taskbar
- ✅ Alt+Tab application switcher
- ✅ Window title bar
- ✅ Desktop shortcuts (if created)

## Icon Design

The icon features:
- Dark gray multimeter body with rounded corners
- Digital display showing "5.000 V"
- Red and black probe connectors
- "SDM4055A" brand label
- Measurement mode indicators (V, A, Ω)

The icon is generated programmatically using PySide6's QPainter, ensuring consistency with the application's design.

## Requirements

- Python 3.8+
- PySide6
- PyInstaller
- All other dependencies listed in `requirements.txt`

Install PyInstaller if needed:
```cmd
pip install pyinstaller
```

## Troubleshooting

### Icon still not showing in taskbar

1. **Clear Windows icon cache**:
   ```cmd
   ie4uinit.exe -show
   ```
   Or restart Windows.

2. **Verify icon file exists**:
   Ensure `app_icon.ico` exists in the project directory before building.

3. **Rebuild the executable**:
   Delete the `dist` and `build` folders, then run the build script again.

4. **Check executable properties**:
   Right-click `SDM4055A_Controller.exe` → Properties → Verify the icon appears correctly there.

### Build fails

1. Ensure all dependencies are installed:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. Check that all required directories exist:
   - `gui/`
   - `hardware/`
   - `config/`
