"""
Google Ads MCP Tools - Ad Group Management

Tools for managing ad groups within campaigns.

Includes tools for:
- Creating and organizing ad groups
- Setting ad group bids and budgets
- Updating ad group status
- Ad group performance analysis

Total: 8 tools
"""

from .mcp_tools_ad_groups import register_ad_group_tools

__all__ = ['register_ad_group_tools']
