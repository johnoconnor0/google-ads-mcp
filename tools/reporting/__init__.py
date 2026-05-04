"""
Google Ads MCP Tools - Reporting & Analytics

Tools for performance reporting and data analysis.

Includes tools for:
- Account-level performance reports
- Campaign comparison analysis
- Period-over-period comparison
- Device performance breakdown
- Geographic performance analysis
- Time-based performance reports
- Impression share analysis

Total: 7 tools
"""

from .mcp_tools_reporting import register_reporting_tools

__all__ = ['register_reporting_tools']
