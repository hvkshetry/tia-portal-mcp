# Troubleshooting Guide

This document provides solutions for common issues with the TIA Portal MCP Server.

## Connection Issues

### Unable to connect to TIA Portal

**Symptoms:**
- Error message: "Failed to connect to TIA Portal"
- No TIA Portal instance starts

**Possible solutions:**
1. Ensure TIA Portal is installed on your system
2. Verify that TIA Openness API is installed and enabled
3. Run Claude Desktop and the MCP server with administrator privileges
4. Check if any TIA Portal instances are already running and close them
5. Restart your computer and try again

### Cannot find `tia_portal` module

**Symptoms:**
- Error message: "No module named 'tia_portal'"

**Possible solutions:**
1. Install the TIA Openness API client:
   ```
   pip install -e git+https://github.com/Repsay/tia-openness-api-client.git#egg=tia_portal
   ```
2. If the installation fails, the server will run in simulation mode

## Project Issues

### Cannot open project

**Symptoms:**
- Error message: "Failed to open project"

**Possible solutions:**
1. Verify the project path is correct
2. Ensure the project file exists and has the correct extension (.ap[1-9][0-9])
3. Check if the project is compatible with your TIA Portal version
4. Make sure the project is not already open in another TIA Portal instance
5. Verify you have read access to the project file

### Cannot access PLC or blocks

**Symptoms:**
- Error message: "PLC with name '[name]' not found"
- Error message: "Block '[name]' not found in PLC '[name]'"

**Possible solutions:**
1. Verify the PLC and block names are correct (case-sensitive)
2. Open the project first using the `open_project` tool
3. Check if the PLC is properly configured in the project
4. Ensure the block exists in the specified PLC

## Claude Desktop Integration

### MCP Server not showing up in Claude

**Symptoms:**
- No hammer icon in Claude Desktop
- Claude doesn't acknowledge TIA Portal tools

**Possible solutions:**
1. Verify your Claude Desktop configuration is correct
2. Make sure Claude Desktop is started after saving the configuration
3. Check if the path to the server script is correct in the configuration
4. Run Claude Desktop as administrator
5. Look for error messages in the Claude Desktop logs

### Permission issues

**Symptoms:**
- Error messages about access denied
- Server crashes when trying to access files

**Possible solutions:**
1. Run both Claude Desktop and the TIA Portal MCP Server as administrator
2. Ensure your user account has access to the TIA Portal installation and project files
3. Check Windows User Account Control (UAC) settings

## Operation Issues

### Server keeps running in simulation mode

**Symptoms:**
- Messages about "simulation mode" in logs
- Fake data being returned instead of real project data

**Possible solutions:**
1. Verify TIA Portal is installed
2. Check if the TIA Openness API client is installed correctly
3. Ensure you're running on Windows (TIA Portal is Windows-only)
4. Try reinstalling the TIA Openness API client

### Server crashes or hangs

**Symptoms:**
- The server stops responding
- Error messages in logs
- Claude Desktop disconnects from the server

**Possible solutions:**
1. Check the server logs for specific error messages
2. Verify TIA Portal is still running and responsive
3. Restart the server and Claude Desktop
4. Limit the size/complexity of operations (e.g., don't try to analyze very large projects at once)

## Getting More Help

If you continue to experience issues:

1. Check the server logs for detailed error messages
2. Look for similar issues in the GitHub repository
3. Contact the repository maintainers with detailed information about your issue
