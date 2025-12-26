@echo off
echo Building SDM4055A_Controller executable...
pyinstaller --onefile ^
    --windowed ^
    --name SDM4055A_Controller ^
    --hidden-import qt_material ^
    --add-data "gui;gui" ^
    --add-data "hardware;hardware" ^
    main.py

echo Build complete! Executable is in dist/SDM4055A_Controller.exe
pause
