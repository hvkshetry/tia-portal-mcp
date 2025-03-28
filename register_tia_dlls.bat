@echo off
echo Registering TIA Openness DLLs...
echo This script requires Administrator privileges
echo.

set "TIA_DLL_PATH=C:\Program Files\Siemens\Automation\Portal V17\PublicAPI\V17"
set "TIA_DLL=Siemens.Engineering.dll"
set "TIA_HMI_DLL=Siemens.Engineering.Hmi.dll"

echo Registering %TIA_DLL%...
regsvr32 /s "%TIA_DLL_PATH%\%TIA_DLL%"
if %errorlevel% neq 0 (
    echo Failed to register %TIA_DLL%
    echo Try running this script as Administrator.
) else (
    echo Successfully registered %TIA_DLL%
)

echo.
echo Registering %TIA_HMI_DLL%...
regsvr32 /s "%TIA_DLL_PATH%\%TIA_HMI_DLL%"
if %errorlevel% neq 0 (
    echo Failed to register %TIA_HMI_DLL%
    echo Try running this script as Administrator.
) else (
    echo Successfully registered %TIA_HMI_DLL%
)

echo.
echo Generating COM Type Libraries...
echo This may take a few moments...

python -m comtypes.client.GetModule "%TIA_DLL_PATH%\%TIA_DLL%"
if %errorlevel% neq 0 (
    echo Failed to generate COM Type Library for %TIA_DLL%
) else (
    echo Successfully generated COM Type Library for %TIA_DLL%
)

python -m comtypes.client.GetModule "%TIA_DLL_PATH%\%TIA_HMI_DLL%"
if %errorlevel% neq 0 (
    echo Failed to generate COM Type Library for %TIA_HMI_DLL%
) else (
    echo Successfully generated COM Type Library for %TIA_HMI_DLL%
)

echo.
echo Registration complete.
echo If you encountered errors, please run this script as Administrator.
echo.
pause
