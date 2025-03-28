# TIA Portal Connection Test

This repository contains utilities to diagnose connection issues with TIA Portal:

1. **MCP Server Diagnostics**: Comprehensive diagnostics for MCP server and TIA Portal connections
2. **tia-openness-api-client Test** (Recommended): Uses the open-source tia-openness-api-client Python package
3. **COM-based Test**: Uses direct COM interaction with TIA Portal

These utilities help diagnose connection issues between Python, MCP servers, and TIA Portal.

## Common Features

- Tests connection to TIA Portal
- Opens a TIA Portal project
- Lists PLCs in the project
- Provides detailed error reporting and diagnostics
- Logs system information to help with troubleshooting

## Prerequisites

- Python 3.6 or higher
- TIA Portal installed
- Administrative privileges may be required

## MCP Server Diagnostics

This comprehensive diagnostic tool checks:

- System resources (CPU, memory, disk space)
- Network connectivity and firewall settings
- TIA Portal installation and Openness configuration
- MCP server status and configuration
- TIA Portal connection test using tia-openness-api-client

### Using the Batch File

1. Double-click `run_mcp_diagnostics.bat` to run the diagnostics
2. Review the summary report displayed in the console
3. Check the detailed logs in the `logs` directory

### Using Python Directly

```
python mcp_server_diagnostics.py
```

## tia-openness-api-client Test (Recommended)

This test uses the [tia-openness-api-client](https://github.com/Repsay/tia-openness-api-client) package which provides a more robust and structured interface to TIA Portal.

### Using the Batch File

1. Double-click `run_tia_client_test.bat` to run the test with the default project path
2. To test with a different project, drag and drop the `.ap*` file onto the batch file or run:
   ```
   run_tia_client_test.bat "C:\path\to\your\project.ap17"
   ```

### Using Python Directly

```
python tia_test_with_client.py --project "C:\path\to\your\project.ap17"
```

## COM-based Test (Legacy)

This test uses direct COM interaction with TIA Portal.

### Using the Batch File

1. Double-click `run_tia_test.bat` to run the test with the default project path
2. To test with a different project, drag and drop the `.ap*` file onto the batch file or run:
   ```
   run_tia_test.bat "C:\path\to\your\project.ap17"
   ```

### Using Python Directly

```
python tia_connection_test.py "C:\path\to\your\project.ap17"
```

If no path is provided, the script will use the default path:
```
C:\Users\hvksh\Circle H2O LLC\CBG Meerut - Documents\CBG Meerut Design and Engineering\Automation\CBG_MEERUT_170824\CBG_MEERUT_170824.ap17
```

## Logs

Detailed logs are saved in the `logs` directory with timestamps. These logs include:
- System information (OS, Python version, memory, CPU)
- Connection details and timing
- Error messages and stack traces
- TIA Portal version information
- Project and PLC details

## Common Issues and Solutions

1. **COM Error**: Make sure TIA Portal is installed correctly and the COM objects are registered.
2. **Access Denied**: Try running as administrator.
3. **Project Path Not Found**: Check that the project path is correct and accessible.
4. **TIA Portal Already Running**: Close any open instances of TIA Portal and try again.
5. **Memory Issues**: Check the logs for memory usage and ensure you have enough available RAM.
6. **Firewall Blocking**: Ensure Windows Firewall allows the MCP server and TIA Portal to communicate.
7. **TIA Openness Disabled**: Enable Openness in TIA Portal settings.
8. **MCP Server Not Running**: Check if the MCP server is running and properly configured.

## Troubleshooting

If the test fails:
1. Check the log files in the `logs` directory
2. Look for specific error messages or exceptions
3. Check the system information section for resource constraints
4. Verify TIA Portal is installed and working correctly
5. Try running TIA Portal manually first, then close it and run the test
6. Use the MCP Server Diagnostics to get a comprehensive report of all possible issues

## Dependencies

The scripts automatically install these dependencies if missing:

### MCP Server Diagnostics:
- tia-openness-api-client (for TIA Portal interaction)
- psutil (for system information)

### tia-openness-api-client Test:
- tia-openness-api-client (for TIA Portal interaction)
- psutil (for system information)

### COM-based Test:
- pywin32 (for COM interaction with TIA Portal)
- psutil (for system information)
