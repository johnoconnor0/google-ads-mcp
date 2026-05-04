"""
Google Ads MCP Tools - Audience & Remarketing

Tools for audience targeting and remarketing campaigns.

Includes tools for:
- Creating customer match audiences
- Building remarketing lists
- Managing audience segments
- Uploading customer data
- Audience performance analysis
- In-market and affinity audiences

Total: 10 tools
"""

from .mcp_tools_audiences import register_audience_tools

__all__ = ['register_audience_tools']
