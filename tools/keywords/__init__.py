"""
Google Ads MCP Tools - Keyword Management

Tools for keyword research, management, and optimization.

Includes tools for:
- Adding and removing keywords
- Managing negative keywords
- Updating keyword bids and match types
- Keyword quality score analysis
- Search term mining and analysis
- Keyword idea generation

Total: 14 tools
"""

from .mcp_tools_keywords import register_keyword_tools

__all__ = ['register_keyword_tools']
