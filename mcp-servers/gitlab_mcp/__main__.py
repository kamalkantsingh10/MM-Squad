"""Allow running as: python -m gitlab_mcp.server"""
from gitlab_mcp.server import mcp

mcp.run(transport="stdio")
