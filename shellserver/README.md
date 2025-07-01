# Shell Server - MCP Terminal Tool

A secure MCP (Model Context Protocol) server that provides terminal command execution capabilities to MCP clients like Claude Desktop.

## 🚀 Features

- **Safe Command Execution**: Execute shell commands with built-in security measures
- **Configurable Working Directory**: Run commands in any specified directory
- **Timeout Protection**: Prevent runaway processes with configurable timeouts
- **Comprehensive Error Handling**: Detailed error messages for various failure scenarios
- **Output Formatting**: Clean separation of stdout, stderr, and exit codes

## ⚠️ Security Notice

This tool provides direct access to your system's shell. Use with caution and only in trusted environments. The server includes several safety measures:

- Command parsing using `shlex.split()` to prevent injection attacks
- Configurable timeouts to prevent hanging processes
- Proper error handling for permission and file access issues
- No automatic privilege escalation

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

### Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Using pip
pip install -e .
```

## 🔧 Configuration

### Adding to Claude Desktop

Add this server to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "shellserver": {
      "command": "python",
      "args": ["/path/to/your/shellserver/server.py"]
    }
  }
}
```

Replace `/path/to/your/shellserver/` with the actual path to your shellserver directory.

## 🛠️ Usage

Once configured, the shell server will be available in Claude Desktop. You can ask Claude to run terminal commands like:

- "Run `ls -la` to see the current directory contents"
- "Execute `git status` in the project directory"
- "Run `python --version` to check the Python version"

### Tool Parameters

The terminal tool accepts the following parameters:

- **command** (required): The shell command to execute
- **working_directory** (optional): Directory to run the command in (default: current directory)
- **timeout** (optional): Maximum execution time in seconds (default: 30)

## 📋 Examples

### Basic Commands
```
Command: ls -la
Working Directory: /home/user/projects
Output: [Directory listing with permissions, dates, and file sizes]
```

### With Custom Timeout
```
Command: python long_running_script.py
Working Directory: /home/user/scripts
Timeout: 60
Output: [Script output or timeout after 60 seconds]
```

## 🏗️ Development

### Project Structure

```
shellserver/
├── server.py          # Main MCP server implementation
├── pyproject.toml     # Project configuration and dependencies
├── README.md          # This file
└── uv.lock           # Dependency lock file
```

### Running the Server

```bash
# Run directly
python server.py

# Or using UV
uv run server.py
```

### Testing

You can test the server functionality by running commands directly:

```python
from server import terminal_tool
import asyncio

# Test basic command
result = asyncio.run(terminal_tool("echo 'Hello, World!'"))
print(result)
```

## 🔍 Error Handling

The server handles various error conditions gracefully:

- **Empty Commands**: Returns error for empty or whitespace-only commands
- **Command Not Found**: Handles cases where the specified command doesn't exist
- **Permission Errors**: Provides clear feedback for permission-related issues
- **Timeouts**: Prevents hanging with configurable timeout limits
- **OS Errors**: Catches and reports system-level errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚖️ License

This project is open source. Please check the license file for details.

## 🛡️ Disclaimer

This tool provides direct system access. Users are responsible for:
- Reviewing commands before execution
- Understanding the security implications
- Using appropriate safeguards in production environments
- Ensuring compliance with their organization's security policies

Use at your own risk. The authors are not responsible for any damage caused by improper use of this tool.

