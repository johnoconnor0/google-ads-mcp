"""
Google Ads MCP Tools - Shopping & Performance Max

Tools for Google Shopping campaigns and Performance Max campaigns.

Includes tools for:
- Creating Shopping campaigns
- Managing product groups and bids
- Creating Performance Max campaigns
- Managing PMax asset groups
- Adding creative assets (images, videos)
- Shopping feed optimization
- Performance analysis

Total: 9 tools
"""

from .mcp_tools_shopping_pmax import register_shopping_pmax_tools

__all__ = ['register_shopping_pmax_tools']
