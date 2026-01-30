@echo off
echo Building SDM4055A_Controller executable...

REM Check if icon file exists, if not create it
if not exist app_icon.ico (
    echo Icon file not found. Generating icon...
    python create_icon.py
)

echo Building executable with icon...
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

echo.
echo Build complete! Executable is in dist/SDM4055A_Controller.exe
echo The application icon should now appear correctly in the taskbar.
pause
