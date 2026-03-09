"""Allow running as: python -m delta_macros_mcp.server"""
from delta_macros_mcp.server import mcp

mcp.run(transport="stdio")
