"""Allow running as: python -m cobol_parser_mcp.server"""
from cobol_parser_mcp.server import mcp

mcp.run(transport="stdio")
