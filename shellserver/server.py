#!/usr/bin/env python3
"""
MCP Server with Terminal Tool and Resources

A simple MCP server that exposes a terminal tool allowing users to run shell commands
and provides access to MCP documentation resources.
"""

import subprocess
import shlex
import asyncio
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("shellserver-app")


@mcp.tool()
async def terminal_tool(command: str, working_directory: str = ".", timeout: int = 30) -> str:
    """
    Execute a terminal command safely.
    
    Args:
        command: The shell command to execute
        working_directory: The directory to run the command in (default: current directory)
        timeout: Maximum time to wait for command completion in seconds (default: 30)
    
    Returns:
        The command output including both stdout and stderr
    """
    
    if not command.strip():
        return "Error: Command cannot be empty"
    
    try:
        # Use shlex.split to safely parse the command
        cmd_args = shlex.split(command)
        
        # Run the command with security considerations
        result = subprocess.run(
            cmd_args,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False  # Don't raise exception on non-zero exit code
        )
        
        # Format the output
        output_lines = []
        
        if result.stdout:
            output_lines.append(f"STDOUT:\n{result.stdout}")
        
        if result.stderr:
            output_lines.append(f"STDERR:\n{result.stderr}")
        
        output_lines.append(f"Exit Code: {result.returncode}")
        
        return "\n".join(output_lines) if output_lines else "Command executed successfully with no output"
        
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except FileNotFoundError:
        return f"Error: Command not found: {cmd_args[0] if cmd_args else 'unknown'}"
    except PermissionError:
        return "Error: Permission denied"
    except OSError as e:
        return f"Error: OS error occurred: {e}"
    except Exception as e:
        return f"Error: Unexpected error occurred: {e}"


@mcp.resource("file://mcpreadme.md")
def get_mcp_readme() -> str:
    """
    Get the MCP Python SDK documentation.
    
    Returns:
        The contents of the MCP Python SDK README file
    """
    try:
        # Get the path to the resources directory
        current_dir = Path(__file__).parent
        readme_path = current_dir / "resources" / "mcpreadme.md"
        
        if not readme_path.exists():
            return "Error: MCP README file not found"
        
        # Read and return the file contents
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except Exception as e:
        return f"Error reading MCP README: {e}"


if __name__ == "__main__":
    # Run the server
    mcp.run("stdio")
