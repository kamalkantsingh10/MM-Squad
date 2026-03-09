"""Delta Macros MCP Server — macro library parsing and search."""

from pathlib import Path

from fastmcp import FastMCP
from shared.config_loader import load_server_config, load_server_env, setup_logging

_SERVER_DIR = Path(__file__).parent
load_server_env(_SERVER_DIR)

logger = setup_logging("delta-macros-mcp", _SERVER_DIR)
config = load_server_config(_SERVER_DIR)

mcp = FastMCP("delta-macros-mcp")

if __name__ == "__main__":
    mcp.run(transport="stdio")
