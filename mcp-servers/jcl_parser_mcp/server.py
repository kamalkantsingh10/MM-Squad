"""JCL Parser MCP Server — JOB/STEP/DD statement parsing."""

from pathlib import Path

from fastmcp import FastMCP
from shared.config_loader import load_server_config, load_server_env, setup_logging

_SERVER_DIR = Path(__file__).parent
load_server_env(_SERVER_DIR)

logger = setup_logging("jcl-parser-mcp", _SERVER_DIR)
config = load_server_config(_SERVER_DIR)

mcp = FastMCP("jcl-parser-mcp")

if __name__ == "__main__":
    mcp.run(transport="stdio")
