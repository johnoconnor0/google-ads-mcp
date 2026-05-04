"""
Google Ads MCP Tools - Local & App Campaigns

Tools for local business campaigns and mobile app promotion.

Includes tools for:
- Creating local campaigns for store visits
- Creating app campaigns for mobile apps
- Managing local extensions
- Local campaign performance analysis
- App campaign optimization

Total: 6 tools
"""

from .mcp_tools_local_app import register_local_app_tools

__all__ = ['register_local_app_tools']
