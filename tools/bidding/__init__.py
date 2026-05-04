"""
Google Ads MCP Tools - Bidding Strategy Management

Tools for managing bidding strategies and bid adjustments.

Includes tools for:
- Setting automated bidding strategies (Target CPA, Target ROAS, Maximize Conversions)
- Managing portfolio bidding strategies
- Device bid adjustments
- Location bid adjustments
- Demographic bid adjustments
- Bid simulation and forecasting

Total: 11 tools
"""

from .mcp_tools_bidding import register_bidding_tools

__all__ = ['register_bidding_tools']
