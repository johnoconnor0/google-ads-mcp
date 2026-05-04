"""
Google Ads MCP Tools - Campaign Management

Tools for creating, managing, and optimizing Google Ads campaigns.

Includes tools for:
- Creating campaigns (Search, Display, Video, Shopping, PMax)
- Managing campaign settings and budgets
- Configuring targeting options (location, language, devices)
- Setting ad schedules and bid strategies
- Campaign performance analysis

Total: 13 tools
"""

from .mcp_tools_campaigns import register_campaign_tools

__all__ = ['register_campaign_tools']
