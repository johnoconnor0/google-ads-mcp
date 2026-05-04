# Google Ads MCP Server - Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install google-ads mcp httpx pydantic google-auth-oauthlib
```

### Step 2: Generate OAuth Token
```bash
python generate_refresh_token.py
```

Follow the prompts to get your refresh token. **Save it securely!**

### Step 3: Configure Claude Desktop

Edit your Claude Desktop config file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add:
```json
{
  "mcpServers": {
    "google-ads": {
      "command": "python",
      "args": ["/full/path/to/google_ads_mcp.py"]
    }
  }
}
```

### Step 4: Restart Claude Desktop

### Step 5: Initialize Connection

Tell Claude:
```
Initialize my Google Ads connection with:
- Developer Token: YOUR_DEVELOPER_TOKEN
- Client ID: YOUR_CLIENT_ID.apps.googleusercontent.com
- Client Secret: YOUR_CLIENT_SECRET
- Refresh Token: YOUR_REFRESH_TOKEN
```

Done! 🎉

---

## 📊 Example Conversations

### Getting Started - Account Overview

**You:** "Show me all my Google Ads accounts"

**Claude:** Uses `google_ads_list_accounts` to display:
```
# Google Ads Accounts

## My Main Business Account
- Customer ID: 1234567890
- Currency: USD
- Timezone: America/Los_Angeles
- Status: ENABLED

## Client Account 1
- Customer ID: 9876543210
- Currency: EUR
- Timezone: Europe/London
- Status: ENABLED
```

---

### Campaign Performance Analysis

**You:** "Analyze campaign performance for account 1234567890 for the last 30 days"

**Claude:** Calls `google_ads_campaign_performance` and provides:
```
# Campaign Performance Report

## Summary
- Total Campaigns: 5
- Total Cost: $12,458.33
- Total Clicks: 3,421
- Total Impressions: 145,892
- Total Conversions: 127.5
- Average CPC: $3.64
- Cost per Conversion: $97.71

## Campaign Details

### Brand Campaign (ENABLED)
- Cost: $5,234.12
- Clicks: 1,543
- CTR: 2.45%
- Conversions: 67.2
- Cost per Conversion: $77.89

### Search Campaign - Product A (ENABLED)
- Cost: $4,123.45
- Clicks: 1,123
- CTR: 1.87%
- Conversions: 42.3
- Cost per Conversion: $97.48
...
```

---

### Finding Optimization Opportunities

**You:** "Which campaigns are spending the most with poor conversion rates?"

**Claude:** Uses `google_ads_campaign_performance` with analysis:
```
Looking at your high-spend campaigns:

1. **Shopping Campaign** - Needs attention ⚠️
   - Spending: $3,456/month
   - Conversion Rate: 0.8% (below 1.5% target)
   - Recommendation: Review product feed, adjust bids

2. **Generic Keywords Campaign**
   - Spending: $2,890/month
   - Conversion Rate: 1.2%
   - Recommendation: Add negative keywords, tighten targeting
```

---

### Keyword Analysis

**You:** "Show me keyword performance for campaign 12345, focusing on quality scores"

**Claude:** Calls `google_ads_keyword_performance`:
```
# Keyword Performance Report

## Low Quality Score Keywords (Needs Improvement)

### "buy products online" (BROAD)
- Quality Score: 3/10 ⚠️
- Cost: $234.56
- Clicks: 45 | Impressions: 2,341
- CTR: 1.92%
- Avg Position: 4.2
- Action: Improve ad relevance or pause

### "cheap deals" (PHRASE)
- Quality Score: 4/10
- Cost: $189.23
- Clicks: 67 | Impressions: 3,456
- CTR: 1.94%
- Action: Consider more specific variations

## High Performers (Keep & Optimize)

### "specific product name" (EXACT)
- Quality Score: 9/10 ✓
- Cost: $456.78
- Clicks: 123 | Impressions: 4,567
- CTR: 2.69%
- Conversions: 23
- Action: Increase bid to gain more volume
```

---

### Search Terms Discovery

**You:** "What search terms are triggering my ads? Show me opportunities for new keywords and negative keywords"

**Claude:** Uses `google_ads_search_terms`:
```
# Search Terms Report - Insights

## 🎯 High-Value Terms (Add as Exact Keywords)

1. "professional business software pricing"
   - Matched: business software (BROAD)
   - Impressions: 234 | Clicks: 12
   - CTR: 5.13% | Conversions: 3
   - Action: Add as exact match keyword

2. "best enterprise crm 2025"
   - Matched: crm software (PHRASE)
   - Impressions: 189 | Clicks: 15
   - CTR: 7.94% | Conversions: 4
   - Action: Create dedicated ad group

## 🚫 Negative Keyword Candidates

1. "free business software"
   - Impressions: 567 | Clicks: 23
   - Cost: $67.89 | Conversions: 0
   - Action: Add "free" as negative keyword

2. "open source alternatives"
   - Impressions: 234 | Clicks: 8
   - Cost: $23.45 | Conversions: 0
   - Action: Add as negative keyword phrase
```

---

### Budget Management

**You:** "My Brand campaign (ID 98765) is performing really well. Increase its budget to $150 per day"

**Claude:** Calls `google_ads_update_campaign_budget`:
```
✓ Successfully updated budget for campaign 98765 to $150.00/day

The campaign will start spending from the new budget within a few hours.
Monitor performance closely for the next 3-5 days to see the impact.
```

---

### Pause Underperforming Campaign

**You:** "The 'Test Campaign' (ID 11111) isn't working. Pause it for now"

**Claude:** Uses `google_ads_update_campaign_status`:
```
✓ Successfully paused campaign 11111

Campaign ads will stop showing immediately. You can re-enable it anytime
when you're ready to test with new settings or creative.
```

---

### Optimization Recommendations

**You:** "What does Google recommend for optimizing my account 1234567890?"

**Claude:** Calls `google_ads_recommendations`:
```
# Google Ads Recommendations

Total Recommendations: 12

1. **KEYWORD_EXPANSION**
   - Impact: High
   - Add 15 new keyword suggestions to your Search campaigns
   - Estimated additional conversions: 8-12 per month

2. **TARGET_CPA_OPT**
   - Impact: Medium
   - Adjust Target CPA from $95 to $87
   - Based on recent conversion performance

3. **RESPONSIVE_SEARCH_AD**
   - Impact: High
   - Switch to responsive search ads for better performance
   - Campaigns: Brand, Product A

4. **BUDGET_RECOMMENDATION**
   - Impact: High
   - Campaign "Brand" is limited by budget
   - Suggested budget: $180/day (current: $120/day)
   - Could gain 23% more conversions
```

---

### Cross-Campaign Analysis

**You:** "Compare performance across all my ad groups to find winners and losers"

**Claude:** Uses `google_ads_ad_group_performance`:
```
# Ad Group Performance Analysis

## Top Performers 🏆

1. **Brand - Exact Match** (Campaign: Brand)
   - Cost: $2,345 | Conversions: 45.6
   - Conversion Rate: 12.3%
   - CPA: $51.43
   - Status: Keep optimizing, consider scaling

2. **High Intent Keywords** (Campaign: Search)
   - Cost: $1,890 | Conversions: 32.1
   - Conversion Rate: 8.7%
   - CPA: $58.88
   - Status: Performing well

## Needs Improvement ⚠️

1. **Generic Terms** (Campaign: Search)
   - Cost: $1,234 | Conversions: 4.2
   - Conversion Rate: 0.9%
   - CPA: $293.81
   - Action: Pause and restructure with tighter keywords

2. **Broad Match Test** (Campaign: Test)
   - Cost: $876 | Conversions: 2.1
   - Conversion Rate: 0.6%
   - CPA: $417.14
   - Action: Consider pausing or switch to phrase match
```

---

### Advanced Custom Query

**You:** "Run this custom query to get my top converting campaigns by hour of day:

SELECT 
  campaign.name,
  segments.hour,
  metrics.conversions,
  metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
ORDER BY metrics.conversions DESC"

**Claude:** Uses `google_ads_custom_query`:
```json
{
  "results": [
    {
      "campaign.name": "Brand Campaign",
      "segments.hour": "14",
      "metrics.conversions": "12.5",
      "metrics.cost_micros": "345678900"
    },
    {
      "campaign.name": "Brand Campaign",
      "segments.hour": "15",
      "metrics.conversions": "11.2",
      "metrics.cost_micros": "312456700"
    },
    ...
  ],
  "count": 168
}
```

**Claude's Analysis:**
"Your campaigns convert best between 2-4 PM (hours 14-15), with Brand 
Campaign leading. Consider dayparting bid adjustments to increase bids 
during these peak hours."

---

## 💡 Pro Tips

### 1. Regular Health Checks
**Weekly:** "Show me campaign performance for the last 7 days and highlight any issues"

### 2. Budget Reallocation
**Monthly:** "Which campaigns should I increase/decrease budgets for based on performance?"

### 3. Search Terms Mining
**Bi-weekly:** "Find new keyword opportunities and negative keywords from search terms"

### 4. Quality Score Monitoring
**Monthly:** "Show me all keywords with quality score below 5"

### 5. Competitive Analysis
**Monthly:** "What are my average positions and how can I improve them?"

### 6. Conversion Tracking
**Weekly:** "Which campaigns have the best cost per conversion?"

### 7. Seasonal Adjustments
**As needed:** "Based on performance, what budget changes should I make for the holiday season?"

---

## 🎯 Common Workflows

### New Campaign Launch Review
```
1. "Show performance for campaign [ID] for last 7 days"
2. "Get search terms report for campaign [ID]"
3. "What keywords have quality score below 6?"
4. "Show me Google's recommendations"
```

### Monthly Optimization
```
1. "Campaign performance last 30 days for account [ID]"
2. "Which campaigns are limited by budget?"
3. "Search terms report - find negative keywords"
4. "Compare ad group performance across campaigns"
```

### Budget Planning
```
1. "Show all campaigns sorted by cost"
2. "Which campaigns have best ROI?"
3. "Recommend budget adjustments based on performance"
```

### Crisis Management
```
1. "Which campaigns are spending the most today?"
2. "Show campaigns with conversion rate below 1%"
3. "Pause all test campaigns immediately"
```

---

## 🔍 Advanced Use Cases

### A/B Test Analysis
Track performance of test campaigns vs. control campaigns

### Seasonal Strategy
Analyze historical data to plan for peak seasons

### Multi-Account Management
Compare performance across different accounts in your MCC

### Custom Reporting
Build custom dashboards using JSON format output

### Automated Alerts
Set up rules to check for issues and alert you

---

## Need Help?

- Check README.md for detailed documentation
- Use Google Ads Query Builder for custom queries
- Review Google Ads API documentation
- Test with small date ranges first
- Start with markdown format for readability

Happy optimizing! 🚀



