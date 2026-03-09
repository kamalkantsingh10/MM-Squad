"""Allow running as: python -m specdb_mcp.server"""
from specdb_mcp.server import mcp

mcp.run(transport="stdio")
