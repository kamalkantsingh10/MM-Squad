"""Allow running as: python -m jcl_parser_mcp.server"""
from jcl_parser_mcp.server import mcp

mcp.run(transport="stdio")
