@echo off
echo Installing TIA Openness API Client...
echo.

:: Add the source directory to PYTHONPATH
set "REPO_PATH=%~dp0\src\tia-portal"
echo Using repository at: %REPO_PATH%

:: Check if the repository exists
if not exist "%REPO_PATH%" (
    echo Cloning repository...
    git clone --quiet https://github.com/Repsay/tia-openness-api-client.git "%REPO_PATH%"
    if %errorlevel% neq 0 (
        echo Failed to clone repository.
        pause
        exit /b 1
    )
)

echo Setting up TIA client in development mode...
cd "%REPO_PATH%"

:: Install the package in development mode
pip install -e .
if %errorlevel% neq 0 (
    echo.
    echo Warning: There was an issue installing the package.
    echo The server may still work by using the path modification.
    echo.
)

:: Create .pth file to add to Python path if needed
set "SITE_PACKAGES=%APPDATA%\Python\Python313\site-packages"
if not exist "%SITE_PACKAGES%" (
    mkdir "%SITE_PACKAGES%"
)

echo %REPO_PATH% > "%SITE_PACKAGES%\tia_portal.pth"
echo Created path file at: "%SITE_PACKAGES%\tia_portal.pth"

echo.
echo Installation completed!
echo Run the test_tia_client.py script to verify installation.
echo.
pause
