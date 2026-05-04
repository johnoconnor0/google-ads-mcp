"""
Google Ads MCP Tools - Batch Operations

Tools for bulk operations and imports/exports.

Includes tools for:
- Batch campaign creation
- Batch ad group creation
- Batch ad creation
- Batch keyword addition
- Bulk budget updates
- Bulk bid updates
- Bulk status changes
- CSV export/import
- Mass data operations

Total: 11 tools
"""

from .mcp_tools_batch import register_batch_tools

__all__ = ['register_batch_tools']
