@echo off
echo Installing TIA Portal MCP Server...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Please install Python 3.10 or higher.
    echo Visit https://www.python.org/downloads/ to download and install Python.
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo Found Python %pyver%

:: Install requirements
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install requirements!
    pause
    exit /b 1
)

:: Try to install TIA Openness API client
echo.
echo Attempting to install TIA Openness API client...
pip install -e git+https://github.com/Repsay/tia-openness-api-client.git#egg=tia_portal
if %errorlevel% neq 0 (
    echo.
    echo Note: Failed to install TIA Openness API client.
    echo The server will run in simulation mode.
    echo.
) else (
    echo.
    echo TIA Openness API client installed successfully.
    echo.
)

:: Create Claude Desktop config if it doesn't exist
set "configdir=%APPDATA%\Claude"
set "configfile=%configdir%\claude_desktop_config.json"

if not exist "%configdir%" (
    echo Creating Claude Desktop config directory...
    mkdir "%configdir%"
)

:: Get current directory
set "serverpath=%~dp0server.py"

:: Check if config file exists
if not exist "%configfile%" (
    echo Creating new Claude Desktop config file...
    echo {> "%configfile%"
    echo   "mcpServers": {>> "%configfile%"
    echo     "tia-portal": {>> "%configfile%"
    echo       "command": "python",>> "%configfile%"
    echo       "args": ["%serverpath:\=\\%"]>> "%configfile%"
    echo     }>> "%configfile%"
    echo   }>> "%configfile%"
    echo }>> "%configfile%"
) else (
    echo.
    echo Claude Desktop config file already exists.
    echo Please manually add the following to your Claude Desktop config file:
    echo.
    echo "tia-portal": {
    echo   "command": "python",
    echo   "args": ["%serverpath:\=\\%"]
    echo }
    echo.
)

echo.
echo Installation complete!
echo To run the server, use run_server.bat or python server.py
echo.
pause
