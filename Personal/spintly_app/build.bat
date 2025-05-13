@echo off
echo Creating necessary directories...
mkdir static 2>nul
mkdir uploads 2>nul
mkdir data 2>nul

echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --clean spintly_app.spec

echo Build complete!
pause 