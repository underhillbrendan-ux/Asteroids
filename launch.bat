@echo off
:: Step 1: Ensure PyInstaller is installed
echo Checking for PyInstaller...
pip install --upgrade pip
pip install pyinstaller

:: Step 2: Clear old build folders to avoid compilation conflicts
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Step 3: Compile the Pygame script into an EXE
echo Packaging Pygame into EXE...
python -m PyInstaller --onefile --noconsole --add-data "assets;assets" main.py

echo Done! Check the 'dist' folder for your executable.
pause