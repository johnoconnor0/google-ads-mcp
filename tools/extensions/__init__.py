"""
Google Ads MCP Tools - Ad Extensions

Tools for managing ad extensions and additional information.

Includes tools for:
- Creating sitelink extensions
- Creating callout extensions
- Creating call extensions
- Creating structured snippets
- Creating price extensions
- Creating promotion extensions
- Managing extension performance

Total: 8 tools
"""

from .mcp_tools_extensions import register_extension_tools

__all__ = ['register_extension_tools']
