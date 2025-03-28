"""
Simplified TIA Portal MCP Server for Reading PLC Code

This server provides read-only access to TIA Portal projects for examining SCL and LAD logic.
It is optimized for stability and reliability when accessing code blocks.
"""

import os
import sys
import logging
from timeout_util import timeout, TimeoutException
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# Add TIA Portal client to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'tia-portal'))

from mcp.server.fastmcp import FastMCP

# Set up logging with clear timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"tia_portal_mcp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    ]
)
logger = logging.getLogger("tia_portal_mcp")

# Initialize FastMCP server
mcp = FastMCP("tia-portal-reader")

# Global variables
portal = None  # Will hold TIA Portal instance
project = None  # Will hold current project
connected = False  # Connection status

# Import TIA Portal client
try:
    import tia_portal.config as tia_config
    from tia_portal import Client
    logger.info("TIA Portal client imported successfully")
except ImportError as e:
    logger.error(f"TIA Portal client not available: {e}. Server cannot run without it.")
    sys.exit(1)

# Check if we're running on Windows, which is required for TIA Portal
if sys.platform != "win32":
    logger.error("TIA Portal requires Windows. Server cannot run on this platform.")
    sys.exit(1)

# Import our custom timeout utility for cross-platform support

# Helper Functions
def find_plc(plc_name):
    """Find a PLC by name in the current project."""
    global project
    
    if project is None:
        logger.warning("Attempted to find PLC but no project is open")
        return None
    
    try:    
        devices = project.get_devices()
        for device in devices:
            try:
                if device.is_plc() and device.get_plc().name == plc_name:
                    return device.get_plc()
            except Exception as e:
                logger.warning(f"Error checking device {device.name}: {str(e)}")
                continue
        
        logger.warning(f"PLC '{plc_name}' not found in project")
        return None
    except Exception as e:
        logger.error(f"Error finding PLC: {str(e)}")
        return None

def format_device_info(device):
    """Format device information as a string."""
    try:
        info = [f"Device: {device.name} ({device.type_name})"]
        
        try:
            if device.is_plc():
                plc = device.get_plc()
                info.append(f"  PLC: {plc.name}")
                
                # Get program blocks
                for block_folder in ["Program blocks", "System blocks", "Technology objects"]:
                    try:
                        blocks = plc.software.get_blocks_folder(block_folder).get_blocks()
                        info.append(f"    {block_folder}:")
                        
                        for i, block in enumerate(blocks):
                            try:
                                if i < 50:  # Limit number of blocks to avoid overwhelming responses
                                    info.append(f"      {block.name} ({block.type}): {block.language}")
                                elif i == 50:
                                    info.append(f"      ... and {len(blocks) - 50} more blocks")
                                    break
                            except Exception as block_error:
                                logger.warning(f"Error getting block info: {str(block_error)}")
                                continue
                    except Exception as folder_error:
                        logger.warning(f"Error accessing folder {block_folder}: {str(folder_error)}")
                        # Some folders might not exist
                        continue
        except Exception as plc_error:
            logger.warning(f"Error processing PLC info: {str(plc_error)}")
        
        return "\n".join(info)
    except Exception as e:
        logger.error(f"Error formatting device info: {str(e)}")
        return f"Error formatting device info: {str(e)}"

# Core functions
@mcp.tool()
async def connect_to_tia() -> str:
    """
    Connect to TIA Portal with simplified error handling.
    
    Returns:
        Connection status message
    """
    global portal, connected
    
    try:
        # Load configuration with error handling and timeout
        try:
            with timeout(10):
                tia_config.load()
                logger.info("TIA Portal configuration loaded")
        except TimeoutException as te:
            logger.warning(f"TIA config loading timed out: {str(te)}")
            return f"TIA config loading timed out after 10 seconds"
        except Exception as e:
            logger.warning(f"Error loading TIA config: {e}")
        
        # Create client with error handling and timeout
        try:
            with timeout(15):
                portal = Client()
                logger.info("TIA Portal client created successfully")
                connected = True
                return "Successfully connected to TIA Portal instance"
        except TimeoutException as te:
            logger.error(f"TIA Portal client creation timed out: {str(te)}")
            return f"TIA Portal client creation timed out after 15 seconds"
        except Exception as e:
            logger.error(f"Failed to create TIA Portal client: {str(e)}")
            return f"Failed to connect to TIA Portal: {str(e)}"
    except Exception as e:
        logger.error(f"Connection error: {str(e)}")
        return f"Failed to connect to TIA Portal: {str(e)}"

@mcp.tool()
async def open_project(project_path: str) -> str:
    """
    Open a TIA Portal project - simplified version.
    
    Args:
        project_path: Path to .ap[1-9][0-9] project file or project directory
    
    Returns:
        Project open status message
    """
    global portal, project
    
    if portal is None:
        try:
            # Try to connect automatically
            result = await connect_to_tia()
            logger.info(f"Auto-connect result: {result}")
        except Exception as e:
            logger.error(f"Auto-connect failed: {str(e)}")
            return "Not connected to TIA Portal. Use connect_to_tia tool first."
    
    try:
        # Extract directory and project name from path
        project_dir = os.path.dirname(project_path)
        project_name = os.path.basename(project_path).split('.')[0]
        
        logger.info(f"Attempting to open project: {project_name} from {project_dir}")
        
        # Try to open with robust error handling and timeout
        try:
            # Try single argument version first with timeout
            try:
                with timeout(60):  # Projects can take a while to open
                    project = portal.open_project(project_path)
                    logger.info(f"Project opened with single argument approach")
                    return f"Successfully opened project: {os.path.basename(project_path)}"
            except TimeoutException as te:
                logger.warning(f"Single argument open timed out: {str(te)}")
                return f"Project opening timed out after 60 seconds"
            except Exception as single_arg_error:
                logger.warning(f"Single argument open failed: {str(single_arg_error)}")
                
                # Try two-argument version with timeout
                with timeout(60):
                    project = portal.open_project(project_dir, project_name)
                    logger.info(f"Project opened with two-argument approach")
                    return f"Successfully opened project: {project_name}"
        except TimeoutException as te:
            logger.error(f"Two-argument open timed out: {str(te)}")
            return f"Project opening timed out after 60 seconds"
        except Exception as open_error:
            logger.error(f"Both open approaches failed: {str(open_error)}")
            raise
    except Exception as e:
        logger.error(f"Failed to open project: {str(e)}")
        return f"Failed to open project: {str(e)}"

@mcp.tool()
async def get_plc_list() -> str:
    """
    Get the list of all PLCs in the current project.
    
    Returns:
        List of PLC names in the project
    """
    global project
    
    if project is None:
        return "No project is currently open"
    
    try:
        logger.info("Getting list of PLCs in the project")
        plcs = []
        
        # Get devices with timeout
        try:
            with timeout(20):
                devices = project.get_devices()
                
                for device in devices:
                    if device.is_plc():
                        plc = device.get_plc()
                        plcs.append(plc.name)
        except TimeoutException as te:
            logger.error(f"Getting devices timed out: {str(te)}")
            return f"Getting devices timed out after 20 seconds"
        
        if not plcs:
            logger.info("No PLCs found in the project")
            return "No PLCs found in the project"
        
        logger.info(f"Found {len(plcs)} PLCs in the project")
        result = ["PLCs in the project:"]
        for plc_name in plcs:
            result.append(f"- {plc_name}")
        
        return "\n".join(result)
    except Exception as e:
        logger.error(f"Error getting PLC list: {str(e)}")
        return f"Error getting PLC list: {str(e)}"

@mcp.tool()
async def list_blocks(plc_name: str) -> str:
    """
    List all available blocks in a PLC.
    
    Args:
        plc_name: Name of the PLC
    
    Returns:
        List of blocks with their types and languages
    """
    global project
    
    if project is None:
        return "No project is currently open"
    
    try:
        # Find the specified PLC with timeout
        plc = None
        try:
            with timeout(15):
                plc = find_plc(plc_name)
                if plc is None:
                    return f"PLC with name '{plc_name}' not found"
        except TimeoutException as te:
            logger.error(f"Finding PLC timed out: {str(te)}")
            return f"Finding PLC '{plc_name}' timed out after 15 seconds"
        
        # Get all software blocks with timeout
        try:
            with timeout(20):
                software = plc.software
                all_blocks = software.get_all_blocks(True)
                
                result = [f"Blocks in PLC '{plc_name}':\n"]
                
                for block in all_blocks:
                    try:
                        result.append(f"{block.name} ({block.type}): {block.language}")
                    except Exception as block_error:
                        logger.warning(f"Error getting block info: {str(block_error)}")
                        result.append(f"{block.name}: Unknown language")
                
                logger.info(f"Found {len(all_blocks)} blocks in PLC '{plc_name}'")
                return "\n".join(result)
        except TimeoutException as te:
            logger.error(f"Getting blocks timed out: {str(te)}")
            return f"Getting blocks for PLC '{plc_name}' timed out after 20 seconds"
        except Exception as blocks_error:
            logger.error(f"Error getting blocks: {str(blocks_error)}")
            return f"Error getting blocks: {str(blocks_error)}"
    except Exception as e:
        logger.error(f"Error listing blocks: {str(e)}")
        return f"Error listing blocks: {str(e)}"

@mcp.tool()
async def read_block_code(plc_name: str, block_name: str) -> str:
    """
    Read the code from a specific block (SCL or LAD) in a PLC.
    
    Args:
        plc_name: Name of the PLC
        block_name: Name of the block to analyze
    
    Returns:
        Block code as text or error message
    """
    global project
    
    if project is None:
        return "No project is currently open"
    
    try:
        logger.info(f"Attempting to read code for block '{block_name}' in PLC '{plc_name}'")
        
        # Find the specified PLC with timeout
        plc = None
        try:
            with timeout(15):
                plc = find_plc(plc_name)
                if plc is None:
                    return f"PLC with name '{plc_name}' not found"
        except TimeoutException as te:
            logger.error(f"Finding PLC timed out: {str(te)}")
            return f"Finding PLC '{plc_name}' timed out after 15 seconds"
        
        # Find the specified block with timeout
        block = None
        try:
            with timeout(20):
                for folder_name in ["Program blocks", "System blocks", "Technology objects"]:
                    try:
                        blocks_folder = plc.software.get_blocks_folder(folder_name)
                        for b in blocks_folder.get_blocks():
                            if b.name == block_name:
                                block = b
                                break
                    except Exception as folder_error:
                        logger.warning(f"Error accessing folder {folder_name}: {str(folder_error)}")
                    
                    if block is not None:
                        break
        except TimeoutException as te:
            logger.error(f"Finding block timed out: {str(te)}")
            return f"Finding block '{block_name}' timed out after 20 seconds"
        
        if block is None:
            return f"Block '{block_name}' not found in PLC '{plc_name}'"
        
        # Get block code with appropriate handling based on language
        if block.language == "SCL":
            try:
                logger.info(f"Reading SCL code for block '{block_name}'")
                with timeout(30):  # Longer timeout for code extraction
                    code = block.get_code()
                    return f"SCL Block {block_name}:\n\n{code}"
            except TimeoutException as te:
                logger.error(f"SCL code retrieval timed out: {str(te)}")
                return f"SCL code retrieval for block '{block_name}' timed out after 30 seconds"
            except Exception as code_error:
                logger.error(f"Error retrieving SCL code: {str(code_error)}")
                return f"Unable to get code for SCL block '{block_name}': {str(code_error)}"
        elif block.language == "LAD":
            try:
                logger.info(f"Reading LAD networks for block '{block_name}'")
                # For LAD, get a network-based description with timeout
                with timeout(30):  # Longer timeout for network analysis
                    networks = block.get_networks()
                    result = f"LAD Block {block_name}:\n\n"
                    
                    for i, network in enumerate(networks):
                        result += f"Network {i+1}: {network.title}\n"
                        result += f"Description: {network.comment}\n"
                        try:
                            result += "Elements: " + ", ".join([elem.name for elem in network.elements]) + "\n\n"
                        except Exception as elem_error:
                            logger.warning(f"Error getting element names: {str(elem_error)}")
                            result += "Elements: [Unable to retrieve element names]\n\n"
                    
                    return result
            except TimeoutException as te:
                logger.error(f"LAD network retrieval timed out: {str(te)}")
                return f"LAD network retrieval for block '{block_name}' timed out after 30 seconds"
            except Exception as lad_error:
                logger.error(f"Error retrieving LAD networks: {str(lad_error)}")
                return f"Unable to get network information for LAD block '{block_name}': {str(lad_error)}"
        else:
            logger.info(f"Block '{block_name}' has unsupported language: {block.language}")
            return f"Block '{block_name}' has language '{block.language}' - detailed viewing not supported, but may still be readable"
    except Exception as e:
        logger.error(f"Error retrieving block code: {str(e)}")
        return f"Error retrieving block code: {str(e)}"

@mcp.tool()
async def reconnect() -> str:
    """
    Force reconnection to TIA Portal
    """
    global portal, project, connected
    
    try:
        logger.info("Attempting to reconnect to TIA Portal")
        # Clean up existing connections with timeout
        if portal is not None:
            try:
                with timeout(15):
                    portal.dispose()
                    logger.info("Disposed existing portal connection")
            except TimeoutException as te:
                logger.warning(f"Portal dispose timed out: {str(te)}")
            except Exception as dispose_error:
                logger.warning(f"Error disposing portal: {str(dispose_error)}")
        
        portal = None
        project = None
        connected = False
        
        # Reconnect
        return await connect_to_tia()
    except Exception as e:
        logger.error(f"Reconnection error: {str(e)}")
        return f"Failed to reconnect: {str(e)}"

# Project Navigation Resource
@mcp.resource(uri="tia://project/structure")
async def project_structure() -> str:
    """
    Get the structure of the currently opened TIA project.
    """
    global portal, project
    
    if project is None:
        return "No project is currently open"
    
    try:
        logger.info("Building project structure overview")
        # Build project structure overview
        structure = [f"Project: {project.name}"]
        
        # Add devices with timeout
        try:
            with timeout(25):
                devices = project.get_devices()
                for device in devices:
                    device_info = format_device_info(device)
                    structure.append(device_info)
            
            return "\n".join(structure)
        except TimeoutException as te:
            logger.error(f"Getting devices timed out: {str(te)}")
            return f"Getting devices timed out after 25 seconds, partial structure:\n" + "\n".join(structure)
    except Exception as e:
        logger.error(f"Error building project structure: {str(e)}")
        return f"Error building project structure: {str(e)}"

# Main execution
if __name__ == "__main__":
    logger.info("Starting TIA Portal Read-Only MCP Server...")
    # Initialize and run the server
    mcp.run(transport='stdio')
