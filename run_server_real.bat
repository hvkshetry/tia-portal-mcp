@echo off
echo Starting TIA Portal MCP Server with real TIA client...

:: Set TIA_AVAILABLE environment variable to force using real client
set TIA_AVAILABLE=TRUE

:: Run the server
python server.py

pause
