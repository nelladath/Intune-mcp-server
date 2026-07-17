"""ASGI entrypoint for native MCP Streamable HTTP transport."""

from intune_mcp_server.server import mcp

# Exposes native MCP over Streamable HTTP at /mcp
app = mcp.streamable_http_app()
