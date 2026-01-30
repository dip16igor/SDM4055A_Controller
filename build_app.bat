@echo off
echo ========================================
echo SDM4055A-SC Controller Build Script
echo ========================================
echo.

REM Step 1: Generate icon file
echo [1/2] Generating application icon...
python create_icon.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to generate icon file
    pause
    exit /b 1
)
echo.

REM Step 2: Build executable
echo [2/2] Building executable with PyInstaller...
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

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable location: dist\SDM4055A_Controller.exe
echo.
echo The application icon should now appear correctly in:
echo - Taskbar
echo - Alt+Tab switcher
echo - Desktop shortcut (if created)
echo.
echo To test the executable, run: dist\SDM4055A_Controller.exe
echo ========================================
pause
