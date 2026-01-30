@echo off
echo Building SDM4055A_Controller executable...
python -m PyInstaller --onefile ^
    --windowed ^
    --name SDM4055A_Controller ^
    --hidden-import qt_material ^
    --hidden-import config ^
    --hidden-import config.config_loader ^
    --add-data "gui;gui" ^
    --add-data "hardware;hardware" ^
    --add-data "config;config" ^
    main.py

echo Build complete! Executable is in dist/SDM4055A_Controller.exe
pause
