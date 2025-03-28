# TIA Portal Read-Only MCP Server

A Machine Communication Protocol (MCP) server for interfacing with Siemens TIA Portal. This server provides read-only access to TIA Portal projects for examining PLC code (SCL and LAD logic), with a focus on stability and reliability.

## Features

- **Read-Only Access**: Safely read PLC code blocks without modifying projects
- **Robust Error Handling**: Comprehensive error handling and timeouts to prevent hanging operations
- **Cross-Platform Timeout Support**: Custom timeout implementation that works on Windows
- **Proper Resource Management**: Clean resource handling to prevent memory leaks
- **Simple API**: Straightforward functions for navigating and reading PLC code

## Prerequisites

- Windows operating system (required for TIA Portal)
- Python 3.6 or higher
- TIA Portal V15 or higher with Openness API installed
- Administrator privileges for installation and execution
- User account part of the 'Siemens TIA Openness' Windows group

## Installation

### Automatic Installation (Recommended)

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/tia-portal-mcp.git
   cd tia-portal-mcp
   ```

2. Run the installation script as administrator:
   ```
   install.bat
   ```

### Manual Installation

1. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Install the TIA Openness API client:
   ```
   pip install -e git+https://github.com/Repsay/tia-openness-api-client.git#egg=tia_portal
   ```

3. Register TIA Portal DLLs (if needed):
   ```
   register_tia_dlls.bat
   ```

## Usage

### Starting the Server

Run the server as administrator:
```
run_server.bat
```

Or directly with Python:
```
python server.py
```

### Connecting to Claude or Other MCP Clients

1. Configure Claude to use this MCP server:
   - Use the server name: `tia-portal`
   - Command: `python`
   - Arguments: `["path/to/server.py"]`

2. In Claude, you can use these functions:
   - `connect_to_tia()` - Connect to TIA Portal
   - `open_project(project_path)` - Open a TIA project
   - `get_plc_list()` - List all PLCs in the current project
   - `list_blocks(plc_name)` - List all blocks in a specific PLC
   - `read_block_code(plc_name, block_name)` - Read the code from a specific block
   - `reconnect()` - Force reconnection to TIA Portal if issues occur

### Example Workflow in Claude

```
connect_to_tia()
open_project("C:/Projects/MyProject.ap16")
get_plc_list()
list_blocks("PLC_1")
read_block_code("PLC_1", "Main")
```

## Limitations

- Read-only access (cannot modify PLC programs)
- Only SCL and LAD languages are fully supported for detailed viewing
- Very large projects might cause timeouts

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [tia-openness-api-client](https://github.com/Repsay/tia-openness-api-client) - Python client for TIA Portal Openness API
- Siemens for the TIA Portal Openness API

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
