"""
Google Ads MCP Server

A comprehensive Model Context Protocol server for Google Ads API integration.
Provides 139+ tools for account analysis, campaign management, audience
targeting, and optimization through modular tool registration.
"""

import json
import os
import sys
import logging
from pathlib import Path
from typing import Optional, List

# ---------------------------------------------------------------------------
# Path & environment setup
# ---------------------------------------------------------------------------

_server_dir = Path(__file__).parent.resolve()
if str(_server_dir) not in sys.path:
    sys.path.insert(0, str(_server_dir))

# Redirect ALL logging to stderr (stdout is reserved for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

try:
    from dotenv import load_dotenv
    load_dotenv(_server_dir / ".env")
except ImportError:
    pass  # dotenv is optional; env vars can be set externally

# ---------------------------------------------------------------------------
# Internal imports
# ---------------------------------------------------------------------------

from mcp.server.fastmcp import FastMCP
from utils.auth_manager import get_auth_manager
from utils.logger import setup_logger, get_logger

logger = setup_logger("google_ads_mcp")

# ---------------------------------------------------------------------------
# FastMCP instance
# ---------------------------------------------------------------------------

mcp = FastMCP("google_ads_mcp")

# ============================================================================
# Core tools (not provided by any modular module)
# ============================================================================


@mcp.tool()
def google_ads_initialize(
    developer_token: str,
    client_id: str,
    client_secret: str,
    refresh_token: str,
    login_customer_id: Optional[str] = None,
) -> str:
    """
    Initialize the Google Ads API connection with OAuth credentials.

    This must be called before using any other Google Ads tools. Provide your
    developer token, OAuth2 credentials, and optionally an MCC login customer ID
    if you're accessing client accounts.

    Args:
        developer_token: API developer token
        client_id: OAuth2 client ID
        client_secret: OAuth2 client secret
        refresh_token: OAuth2 refresh token
        login_customer_id: Optional MCC account ID (without hyphens)

    Returns:
        Confirmation message with initialization status
    """
    try:
        clean_login_id = login_customer_id.replace("-", "") if login_customer_id else None

        auth = get_auth_manager()
        auth.initialize_oauth(
            developer_token=developer_token,
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            login_customer_id=clean_login_id,
        )

        msg = "✓ Google Ads API client initialized successfully.\n"
        if clean_login_id:
            msg += f"✓ Using MCC account: {clean_login_id}\n"
        msg += "\nYou can now use other Google Ads tools to access your account data."
        return msg

    except Exception as exc:
        return f"❌ Initialization failed: {exc}"


@mcp.tool()
def google_ads_list_accounts(
    response_format: str = "markdown",
) -> str:
    """
    List all Google Ads accounts accessible with current credentials.

    Returns details about all accounts you have access to, including customer IDs,
    names, currency codes, and whether they are manager accounts.

    Args:
        response_format: Output format: 'markdown' for readable or 'json' for structured data

    Returns:
        List of accessible accounts with their details
    """
    try:
        client = get_auth_manager().get_client()
        customer_service = client.get_service("CustomerService")
        ga_service = client.get_service("GoogleAdsService")

        accessible = customer_service.list_accessible_customers()

        accounts = []
        for resource_name in accessible.resource_names:
            cid = resource_name.split("/")[-1]
            try:
                rows = ga_service.search(
                    customer_id=cid,
                    query=(
                        "SELECT customer.id, customer.descriptive_name, "
                        "customer.currency_code, customer.time_zone, customer.manager "
                        "FROM customer"
                    ),
                )
                for row in rows:
                    accounts.append({
                        "customer_id": str(row.customer.id),
                        "name": row.customer.descriptive_name,
                        "currency": row.customer.currency_code,
                        "timezone": row.customer.time_zone,
                        "is_manager": row.customer.manager,
                    })
            except Exception:
                accounts.append({"customer_id": cid, "name": "(inaccessible)", "currency": "", "timezone": "", "is_manager": False})

        if response_format == "json":
            return json.dumps(accounts, indent=2)

        out = f"# Accessible Google Ads Accounts ({len(accounts)})\n\n"
        out += "| Customer ID | Name | Currency | Timezone | Type |\n"
        out += "|-------------|------|----------|----------|------|\n"
        for a in accounts:
            t = "MCC" if a["is_manager"] else "Standard"
            out += f"| {a['customer_id']} | {a['name']} | {a['currency']} | {a['timezone']} | {t} |\n"
        return out

    except Exception as exc:
        return f"❌ Failed to list accounts: {exc}"


@mcp.tool()
def google_ads_custom_query(
    customer_id: str,
    query: str,
    response_format: str = "json",
) -> str:
    """
    Execute a custom Google Ads Query Language (GAQL) query.

    For advanced users who want to write their own GAQL queries. Use the
    Google Ads Query Builder to construct queries:
    https://developers.google.com/google-ads/api/fields/latest/overview_query_builder

    Args:
        customer_id: Customer ID (without hyphens)
        query: GAQL query string
        response_format: Output format ('json' or 'markdown')

    Returns:
        Query results in specified format
    """
    try:
        client = get_auth_manager().get_client()
        ga_service = client.get_service("GoogleAdsService")
        clean_id = customer_id.replace("-", "")

        response = ga_service.search(customer_id=clean_id, query=query)

        results = []
        for row in response:
            row_dict = {}
            for field_name in type(row).meta.fields.keys():
                value = getattr(row, field_name, None)
                if value:
                    row_dict[field_name] = str(value)
            results.append(row_dict)

        header = f"# Custom Query Results\n\n**Query**: {query}\n\n**Result Count**: {len(results)}\n\n"

        if response_format == "json":
            return header + json.dumps(results, indent=2, default=str)

        if not results:
            return header + "No results found."

        keys = list(results[0].keys())
        table = "| " + " | ".join(keys) + " |\n"
        table += "| " + " | ".join("---" for _ in keys) + " |\n"
        for r in results:
            table += "| " + " | ".join(str(r.get(k, ""))[:60] for k in keys) + " |\n"
        return header + table

    except Exception as exc:
        return f"❌ Custom query failed: {exc}"


@mcp.tool()
def google_ads_campaign_performance(
    customer_id: str,
    date_range: str = "LAST_30_DAYS",
    campaign_status: Optional[List[str]] = None,
    min_cost: Optional[float] = None,
    limit: int = 50,
    response_format: str = "markdown",
) -> str:
    """
    Get comprehensive performance metrics for campaigns.

    Retrieves key performance indicators including cost, clicks, impressions, CTR,
    conversions, and more for campaigns in the specified date range. Supports
    filtering by status and cost thresholds.

    Args:
        customer_id: Customer ID without hyphens (e.g., '1234567890')
        date_range: Predefined date range (TODAY, YESTERDAY, LAST_7_DAYS,
                    LAST_14_DAYS, LAST_30_DAYS, THIS_MONTH, LAST_MONTH, LAST_90_DAYS)
        campaign_status: Filter by status list e.g. ['ENABLED', 'PAUSED']
        min_cost: Minimum cost filter in currency units
        limit: Maximum number of campaigns to return (1-100)
        response_format: Output format: 'markdown' or 'json'

    Returns:
        Campaign performance data with metrics and analysis
    """
    try:
        client = get_auth_manager().get_client()
        ga_service = client.get_service("GoogleAdsService")
        clean_id = customer_id.replace("-", "")

        query = (
            "SELECT campaign.id, campaign.name, campaign.status, "
            "campaign.advertising_channel_type, campaign_budget.amount_micros, "
            "metrics.impressions, metrics.clicks, metrics.cost_micros, "
            "metrics.conversions, metrics.conversions_value, "
            "metrics.ctr, metrics.average_cpc "
            f"FROM campaign WHERE segments.date DURING {date_range}"
        )

        if campaign_status:
            statuses = ", ".join(f"'{s}'" for s in campaign_status)
            query += f" AND campaign.status IN ({statuses})"
        else:
            query += " AND campaign.status != 'REMOVED'"

        query += f" ORDER BY metrics.cost_micros DESC LIMIT {min(max(limit, 1), 100)}"

        response = ga_service.search(customer_id=clean_id, query=query)

        campaigns = []
        for row in response:
            cost = row.metrics.cost_micros / 1_000_000
            if min_cost is not None and cost < min_cost:
                continue

            convs = row.metrics.conversions
            cpa = cost / convs if convs > 0 else 0
            roas = row.metrics.conversions_value / cost if cost > 0 else 0

            campaigns.append({
                "campaign_id": str(row.campaign.id),
                "name": row.campaign.name,
                "status": row.campaign.status.name,
                "type": row.campaign.advertising_channel_type.name,
                "budget": round(row.campaign_budget.amount_micros / 1_000_000, 2),
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "ctr": round(row.metrics.ctr * 100, 2),
                "avg_cpc": round(row.metrics.average_cpc / 1_000_000, 2),
                "cost": round(cost, 2),
                "conversions": round(convs, 2),
                "conversion_value": round(row.metrics.conversions_value, 2),
                "cpa": round(cpa, 2),
                "roas": round(roas, 2),
            })

        if response_format == "json":
            return json.dumps({"date_range": date_range, "campaigns": campaigns}, indent=2)

        out = f"# Campaign Performance ({date_range})\n\n"
        out += f"**Campaigns**: {len(campaigns)}\n\n"
        out += "| Campaign | Status | Type | Impr | Clicks | CTR | Cost | Conv | CPA | ROAS |\n"
        out += "|----------|--------|------|------|--------|-----|------|------|-----|------|\n"
        for c in campaigns:
            out += (
                f"| {c['name'][:30]} | {c['status']} | {c['type'][:10]} "
                f"| {c['impressions']:,} | {c['clicks']:,} | {c['ctr']}% "
                f"| ${c['cost']:,.2f} | {c['conversions']:.1f} "
                f"| ${c['cpa']:.2f} | {c['roas']:.2f} |\n"
            )

        total_cost = sum(c["cost"] for c in campaigns)
        total_conv = sum(c["conversions"] for c in campaigns)
        total_val = sum(c["conversion_value"] for c in campaigns)
        out += f"\n**Totals**: Cost ${total_cost:,.2f} | Conv {total_conv:.1f} | Value ${total_val:,.2f}"
        if total_cost > 0:
            out += f" | ROAS {total_val / total_cost:.2f}"
        return out

    except Exception as exc:
        return f"❌ Campaign performance query failed: {exc}"


@mcp.tool()
def google_ads_search_terms(
    customer_id: str,
    campaign_id: Optional[str] = None,
    date_range: str = "LAST_30_DAYS",
    limit: int = 100,
    response_format: str = "markdown",
) -> str:
    """
    View actual search queries that triggered your ads.

    Shows the search terms report with performance metrics to identify
    new keyword opportunities and negative keyword candidates.

    Args:
        customer_id: Customer ID without hyphens
        campaign_id: Optional campaign ID to filter
        date_range: Date range for the report
        limit: Maximum number of search terms to return
        response_format: Output format: 'markdown' or 'json'

    Returns:
        Search terms with performance metrics
    """
    try:
        client = get_auth_manager().get_client()
        ga_service = client.get_service("GoogleAdsService")
        clean_id = customer_id.replace("-", "")

        query = (
            "SELECT campaign.name, ad_group.name, "
            "search_term_view.search_term, search_term_view.status, "
            "metrics.impressions, metrics.clicks, metrics.cost_micros, "
            "metrics.conversions "
            f"FROM search_term_view WHERE segments.date DURING {date_range}"
        )

        if campaign_id:
            query += f" AND campaign.id = {campaign_id}"

        query += f" ORDER BY metrics.impressions DESC LIMIT {min(limit, 200)}"

        response = ga_service.search(customer_id=clean_id, query=query)

        terms = []
        for row in response:
            cost = row.metrics.cost_micros / 1_000_000
            imps = row.metrics.impressions
            clicks = row.metrics.clicks
            ctr = (clicks / imps * 100) if imps > 0 else 0

            terms.append({
                "search_term": row.search_term_view.search_term,
                "campaign": row.campaign.name,
                "ad_group": row.ad_group.name,
                "status": row.search_term_view.status.name,
                "impressions": imps,
                "clicks": clicks,
                "ctr": round(ctr, 2),
                "cost": round(cost, 2),
                "conversions": round(row.metrics.conversions, 2),
            })

        if response_format == "json":
            return json.dumps(terms, indent=2)

        out = f"# Search Terms Report ({date_range})\n\n"
        out += f"**Total terms**: {len(terms)}\n\n"
        out += "| Search Term | Campaign | Impr | Clicks | CTR | Cost | Conv | Status |\n"
        out += "|-------------|----------|------|--------|-----|------|------|--------|\n"
        for t in terms:
            out += (
                f"| {t['search_term'][:40]} | {t['campaign'][:20]} "
                f"| {t['impressions']:,} | {t['clicks']:,} | {t['ctr']}% "
                f"| ${t['cost']:.2f} | {t['conversions']:.1f} | {t['status']} |\n"
            )
        return out

    except Exception as exc:
        return f"❌ Search terms query failed: {exc}"


@mcp.tool()
def google_ads_recommendations(
    customer_id: str,
    recommendation_types: Optional[List[str]] = None,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """
    Get AI-powered optimization recommendations from Google.

    Retrieve Google's automated recommendations for improving campaign performance,
    including keyword suggestions, bid adjustments, and budget recommendations.

    Args:
        customer_id: Customer ID without hyphens
        recommendation_types: Filter by recommendation types
            (e.g., ['KEYWORD', 'TARGET_CPA_OPT'])
        limit: Maximum number of recommendations (1-100)
        response_format: Output format: 'markdown' or 'json'

    Returns:
        List of actionable optimization recommendations
    """
    try:
        client = get_auth_manager().get_client()
        ga_service = client.get_service("GoogleAdsService")
        clean_id = customer_id.replace("-", "")

        query = (
            "SELECT recommendation.resource_name, recommendation.type, "
            "recommendation.impact, recommendation.campaign "
            "FROM recommendation "
            "WHERE recommendation.dismissed = FALSE"
        )

        if recommendation_types:
            types_str = ", ".join(f"'{t}'" for t in recommendation_types)
            query += f" AND recommendation.type IN ({types_str})"

        query += f" LIMIT {min(max(limit, 1), 100)}"

        response = ga_service.search(customer_id=clean_id, query=query)

        recs = []
        for row in response:
            recs.append({
                "type": row.recommendation.type.name,
                "campaign": row.recommendation.campaign or "Account-level",
                "impact": str(row.recommendation.impact),
            })

        if response_format == "json":
            return json.dumps(recs, indent=2, default=str)

        out = f"# Optimization Recommendations\n\n"
        out += f"**Total**: {len(recs)}\n\n"
        out += "| Type | Campaign | Impact |\n"
        out += "|------|----------|--------|\n"
        for r in recs:
            out += f"| {r['type']} | {r['campaign'][:30]} | {r['impact'][:50]} |\n"
        return out

    except Exception as exc:
        return f"❌ Recommendations query failed: {exc}"


# ============================================================================
# Register all modular tool modules
# ============================================================================

_TOOL_MODULES = [
    ("campaigns",     "tools.campaigns.mcp_tools_campaigns",         "register_campaign_tools"),
    ("ad_groups",     "tools.ad_groups.mcp_tools_ad_groups",         "register_ad_group_tools"),
    ("keywords",      "tools.keywords.mcp_tools_keywords",           "register_keyword_tools"),
    ("ads",           "tools.ads.mcp_tools_ads",                     "register_ad_tools"),
    ("bidding",       "tools.bidding.mcp_tools_bidding",             "register_bidding_tools"),
    ("automation",    "tools.automation.mcp_tools_automation",       "register_automation_tools"),
    ("audiences",     "tools.audiences.mcp_tools_audiences",         "register_audience_tools"),
    ("conversions",   "tools.conversions.mcp_tools_conversions",     "register_conversion_tools"),
    ("reporting",     "tools.reporting.mcp_tools_reporting",         "register_reporting_tools"),
    ("insights",      "tools.insights.mcp_tools_insights",           "register_insights_tools"),
    ("batch",         "tools.batch.mcp_tools_batch",                 "register_batch_tools"),
    ("shopping_pmax", "tools.shopping_pmax.mcp_tools_shopping_pmax", "register_shopping_pmax_tools"),
    ("extensions",    "tools.extensions.mcp_tools_extensions",       "register_extension_tools"),
    ("local_app",     "tools.local_app.mcp_tools_local_app",         "register_local_app_tools"),
]


def _register_all_modular_tools():
    """Import and register every modular tool module."""
    import importlib

    registered = 0
    for label, module_path, func_name in _TOOL_MODULES:
        try:
            mod = importlib.import_module(module_path)
            register_fn = getattr(mod, func_name)
            register_fn(mcp)
            logger.info(f"  ✓ {label}")
            registered += 1
        except Exception as exc:
            logger.error(f"  ✗ {label}: {exc}")

    logger.info(f"Registered {registered}/{len(_TOOL_MODULES)} modular tool modules")


# ============================================================================
# Auto-initialise from environment
# ============================================================================

def _auto_initialize_from_env():
    """Try to initialise the Google Ads client from .env credentials."""
    dev_token = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
    cid = os.getenv("GOOGLE_ADS_CLIENT_ID")
    csecret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")
    rtoken = os.getenv("GOOGLE_ADS_REFRESH_TOKEN")
    login_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")

    if not all([dev_token, cid, csecret, rtoken]):
        logger.info("Env credentials incomplete – manual google_ads_initialize required")
        return False

    try:
        clean_login_id = login_id.replace("-", "") if login_id else None
        auth = get_auth_manager()
        auth.initialize_oauth(
            developer_token=dev_token,
            client_id=cid,
            client_secret=csecret,
            refresh_token=rtoken,
            login_customer_id=clean_login_id,
        )
        logger.info(f"✓ Auto-initialised from .env (MCC: {clean_login_id or 'none'})")
        return True
    except Exception as exc:
        logger.warning(f"Auto-init failed: {exc} – manual google_ads_initialize required")
        return False


# ============================================================================
# Server startup
# ============================================================================

logger.info("Registering modular tools …")
_register_all_modular_tools()
_auto_initialize_from_env()
logger.info("Google Ads MCP Server ready")


def main() -> None:
    """Run the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()

