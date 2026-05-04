# Google Ads MCP Server - Setup Requirements

**Date:** 2025-12-16
**Purpose:** Complete checklist of everything needed to set up and run the Google Ads MCP server

---

## 1. Google Ads API Access Requirements

### A. Developer Token
**What:** Unique identifier for API access
**Where to Get:** Google Ads account → Tools & Settings → API Center
**Application URL:** https://developers.google.com/google-ads/api/docs/get-started/dev-token
**Approval Time:** Instant for test access, 24-48 hours for production

**Steps:**
1. Sign in to your Google Ads account
2. Navigate to Tools & Settings → Setup → API Center
3. Request a developer token
4. Use test token immediately or wait for production approval

**Cost:** Free

---

### B. OAuth 2.0 Credentials

#### Required Credentials:
1. **Client ID** - Identifies your application
2. **Client Secret** - Secret key for authentication
3. **Refresh Token** - Long-lived access token

#### Setup Steps:

**Step 1: Create Google Cloud Project**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Name it (e.g., "Google Ads MCP Server")

**Step 2: Enable Google Ads API**
1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Ads API"
3. Click "Enable"

**Step 3: Create OAuth Credentials**
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Configure consent screen if prompted:
   - User Type: External (for most cases)
   - App name: "Google Ads MCP Server"
   - Support email: Your email
   - Scopes: Add `https://www.googleapis.com/auth/adwords`
4. Application type: **Desktop app**
5. Name: "Google Ads MCP Client"
6. Click "Create"
7. **Save Client ID and Client Secret** (you'll need these)

**Step 4: Generate Refresh Token**
1. Run the included script:
   ```bash
   python generate_refresh_token.py
   ```
2. Enter your Client ID and Client Secret when prompted
3. Browser will open for authorization
4. Sign in with Google account that has access to Google Ads
5. Grant permissions
6. **Copy and save the refresh token** displayed

**Cost:** Free

---

### C. Google Ads Account Access

**Requirements:**
- Active Google Ads account with campaigns (or create test account)
- Account must be linked to the Google account used for OAuth
- For managing multiple clients: MCC (Manager) account

**Customer ID:**
- Found in Google Ads UI (top right corner)
- Format: `123-456-7890`
- **Important:** Remove hyphens for API use → `1234567890`

**MCC Account (Optional, for managing multiple clients):**
- Create at: https://ads.google.com/home/tools/manager-accounts/
- Free to set up
- Link client accounts under MCC
- Use MCC Customer ID as `login_customer_id` in API calls

---

## 2. Development Environment Requirements

### A. Python Environment

**Required Version:** Python 3.10 or higher

**Check Current Version:**
```bash
python --version
```

**Install Python (if needed):**
- **Windows:** Download from https://www.python.org/downloads/
- **macOS:** `brew install python3`
- **Linux:** `sudo apt-get install python3.10`

---

### B. Python Dependencies

**Installation:**
```bash
# Option 1: Install from requirements.txt
pip install -r requirements.txt

# Option 2: Install individually
pip install google-ads
pip install mcp
pip install httpx
pip install pydantic
pip install google-auth-oauthlib
```

**Required Packages:**
1. **google-ads** (v24.0.0+) - Google Ads API client library
2. **mcp** (v1.1.0+) - Model Context Protocol SDK
3. **httpx** - Modern HTTP client
4. **pydantic** (v2.0+) - Data validation
5. **google-auth-oauthlib** - OAuth authentication

**Verify Installation:**
```bash
pip list | grep -E "(google-ads|mcp|httpx|pydantic|google-auth)"
```

---

### C. Claude Desktop

**Required For:** MCP server integration

**Installation:**
- Download from: https://claude.ai/download
- Available for macOS and Windows

**Configuration File Location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration Template:**
```json
{
  "mcpServers": {
    "google-ads": {
      "command": "python",
      "args": ["c:\\google-mcp\\google_ads_mcp.py"],
      "env": {}
    }
  }
}
```

**Important:**
- Use absolute paths (not relative)
- Windows: Use double backslashes (`\\`) or forward slashes (`/`)
- macOS/Linux: Standard Unix paths

---

## 3. API Version & Compatibility

### Current API Version
**Version:** v22 (latest as of December 2024)
**Current Implementation:** v17+ (needs update)

**Google Ads API Versions:**
- v22 (Latest) - Recommended
- v21 (Supported)
- v20 (Supported)
- v19 (Deprecated soon)

**Update Recommendation:** Update to v22 for latest features and longest support window.

**Migration Path:**
```python
# Current (v17+):
from google.ads.googleads.client import GoogleAdsClient

# Target (v22):
# Same import, update version in queries
# Check breaking changes: https://developers.google.com/google-ads/api/docs/release-notes
```

---

## 4. Testing Requirements

### A. Test Account Setup

**Option 1: Use Existing Account** (Recommended if you have one)
- Use real account with real campaigns
- Start with read-only operations
- Test write operations on low-budget campaigns

**Option 2: Create Test Account**
1. Create new Google Ads account
2. Set up 2-3 test campaigns with minimal budget ($10-50)
3. Create sample ad groups, keywords, ads
4. Let run for a few days to generate data

**Test Account Checklist:**
- ✅ At least 1 active campaign
- ✅ Multiple ad groups
- ✅ Keywords with various match types
- ✅ Active ads (approved)
- ✅ Some historical performance data (7+ days)
- ✅ Conversion tracking set up (optional but helpful)

---

### B. API Testing Tools

**Recommended Tools:**
1. **Google Ads Query Builder**
   - URL: https://developers.google.com/google-ads/api/fields/v22/overview_query_builder
   - Use: Test GAQL queries before implementing

2. **Python Interactive Shell**
   ```bash
   python -i google_ads_mcp.py
   # Test individual functions
   ```

3. **Pytest** (for automated testing)
   ```bash
   pip install pytest pytest-asyncio pytest-mock
   ```

---

## 5. Security Requirements

### A. Credential Storage

**Required Security Measures:**
1. **Never commit credentials to Git**
   - Add to `.gitignore`:
     ```
     *.env
     credentials.json
     google_ads.yaml
     *_credentials.txt
     ```

2. **Use Environment Variables** (recommended)
   ```bash
   # .env file (add to .gitignore)
   GOOGLE_ADS_DEVELOPER_TOKEN=your_token
   GOOGLE_ADS_CLIENT_ID=your_client_id
   GOOGLE_ADS_CLIENT_SECRET=your_secret
   GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token
   GOOGLE_ADS_LOGIN_CUSTOMER_ID=your_mcc_id  # optional
   ```

3. **Use Secrets Manager** (for production)
   - AWS Secrets Manager
   - Google Secret Manager
   - Azure Key Vault
   - HashiCorp Vault

---

### B. Access Control

**Recommendations:**
1. **Principle of Least Privilege**
   - Request only necessary API scopes
   - Use read-only access where possible
   - Limit MCC account access

2. **Multi-Factor Authentication**
   - Enable 2FA on Google account
   - Use application-specific passwords if needed

3. **Regular Token Rotation**
   - Rotate refresh tokens every 90 days
   - Monitor token usage
   - Revoke unused tokens

---

## 6. Network & Infrastructure Requirements

### A. Network Access

**Required Outbound Connections:**
- `googleads.googleapis.com` (Port 443) - API endpoints
- `oauth2.googleapis.com` (Port 443) - Authentication
- `accounts.google.com` (Port 443) - OAuth flow

**Firewall Rules:**
- Allow HTTPS (443) outbound to Google domains
- No inbound connections required

---

### B. Rate Limits & Quotas

**Google Ads API Rate Limits:**
- **Standard Access:** 15,000 operations per day (per developer token)
- **Basic Access:** 15,000 operations per day
- **No daily limit** for read operations (but subject to rate limiting)

**Rate Limit Headers:**
```
ratelimit-limit: 40000
ratelimit-remaining: 39999
ratelimit-reset: 1640000000
```

**Best Practices:**
1. Implement exponential backoff on errors
2. Cache frequently accessed data
3. Use batch operations for bulk changes
4. Monitor quota usage

---

## 7. Monitoring & Logging Requirements

### A. Logging Setup

**Recommended Logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('google_ads_mcp.log'),
        logging.StreamHandler()
    ]
)
```

**What to Log:**
- API requests (customer ID, operation type)
- Authentication events
- Errors and exceptions
- Performance metrics (response times)
- Rate limit warnings

**What NOT to Log:**
- Developer tokens
- Client secrets
- Refresh tokens
- User credentials
- Sensitive customer data

---

### B. Error Tracking

**Recommended Tools:**
- Sentry (https://sentry.io) - Error tracking
- Datadog - APM and monitoring
- CloudWatch (AWS) - Log aggregation
- Application Insights (Azure) - Monitoring

---

## 8. Documentation Requirements

### A. User Documentation

**Required Documents:**
1. ✅ README.md - Setup and overview
2. ✅ QUICKSTART.md - Quick start guide
3. ✅ EXECUTIVE_SUMMARY.md - Project implementation summary
4. ✅ EXECUTIVE_SUMMARY.md - High-level summary
5. ⬜ API_REFERENCE.md - Tool documentation (to be created)
6. ⬜ TROUBLESHOOTING.md - Common issues (to be created)

---

### B. Developer Documentation

**Required Documents:**
1. ✅ CLAUDE.md - Project instructions for Claude
2. ⬜ CONTRIBUTING.md - Contribution guidelines (to be created)
3. ⬜ CHANGELOG.md - Version history (to be created)
4. ⬜ ARCHITECTURE.md - System design (to be created)

---

## 9. Optional Enhancements

### A. Caching Layer (Recommended for Production)

**Options:**
1. **In-Memory Caching** (simple, for single-instance)
   ```bash
   pip install cachetools
   ```

2. **Redis** (recommended for multi-instance)
   ```bash
   pip install redis
   # Requires Redis server
   ```

**Benefits:**
- Reduce API calls
- Improve response times
- Lower quota usage
- Better user experience

---

### B. Database (Optional)

**Use Cases:**
- Store historical performance data
- Cache API responses persistently
- Audit trail of changes
- Custom reporting

**Options:**
- SQLite (simple, file-based)
- PostgreSQL (production-grade)
- MongoDB (document store)

---

### C. Web Interface (Future Enhancement)

**Frameworks:**
- FastAPI - Modern Python web framework
- Streamlit - Quick data apps
- Dash - Analytics dashboards

**Use Cases:**
- Visual campaign builder
- Interactive reports
- Admin dashboard
- API playground

---

## 10. Compliance & Legal Requirements

### A. Google Ads API Policies

**Must Comply With:**
1. **Google Ads API Terms of Service**
   - URL: https://developers.google.com/google-ads/api/terms
   - Review annually
   - Follow usage guidelines

2. **Data Usage Restrictions**
   - Don't share customer data without permission
   - Follow data retention policies
   - Implement data security measures
   - Respect user privacy

3. **Attribution Requirements**
   - Credit Google when displaying data
   - Use official Google Ads branding
   - Follow brand guidelines

---

### B. Data Privacy

**Requirements:**
1. **GDPR Compliance** (if serving EU users)
   - Data processing agreements
   - User consent for data collection
   - Right to data deletion

2. **CCPA Compliance** (if serving California users)
   - Privacy policy
   - User data access rights
   - Opt-out mechanisms

---

## 11. Deployment Checklist

### Pre-Deployment
- [ ] All credentials obtained and tested
- [ ] Development environment set up
- [ ] Dependencies installed
- [ ] Test account created with sample data
- [ ] OAuth flow tested successfully
- [ ] API calls working in development
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Documentation reviewed

### Deployment
- [ ] Claude Desktop installed
- [ ] MCP server configured in Claude Desktop
- [ ] Server started successfully
- [ ] Connection verified
- [ ] Test queries executed
- [ ] Error scenarios tested
- [ ] Performance validated

### Post-Deployment
- [ ] Monitoring enabled
- [ ] Alerts configured
- [ ] Backup procedures established
- [ ] Documentation published
- [ ] Team training completed
- [ ] Support process defined

---

## 12. Quick Reference: Credential Template

```yaml
# google_ads_credentials.yaml (DO NOT COMMIT TO GIT!)

developer_token: "INSERT_YOUR_DEV_TOKEN_HERE"
client_id: "INSERT_CLIENT_ID.apps.googleusercontent.com"
client_secret: "INSERT_CLIENT_SECRET"
refresh_token: "INSERT_REFRESH_TOKEN"
login_customer_id: "1234567890"  # Optional, for MCC accounts
use_proto_plus: false
```

---

## 13. Common Setup Issues & Solutions

### Issue 1: "Developer token not approved"
**Solution:**
- Apply for token at Google Ads API Center
- Use test token for development
- Wait 24-48 hours for production approval

### Issue 2: "Invalid refresh token"
**Solution:**
- Regenerate refresh token using `generate_refresh_token.py`
- Ensure correct Client ID and Secret
- Check OAuth scopes include Google Ads

### Issue 3: "Customer not found"
**Solution:**
- Verify Customer ID format (remove hyphens)
- Ensure account access for authenticated user
- Check if using correct login_customer_id for MCC

### Issue 4: "Insufficient permissions"
**Solution:**
- Verify Google account has access to Google Ads account
- Check developer token access level
- Ensure OAuth scope is correct

### Issue 5: "Rate limit exceeded"
**Solution:**
- Implement request throttling
- Add exponential backoff
- Reduce query frequency
- Use caching

---

## 14. Support Resources

### Official Documentation
- **Google Ads API Docs:** https://developers.google.com/google-ads/api/docs/start
- **Client Libraries:** https://developers.google.com/google-ads/api/docs/client-libs/python
- **Query Language (GAQL):** https://developers.google.com/google-ads/api/docs/query/overview
- **Field Reference:** https://developers.google.com/google-ads/api/fields/v22/overview

### Community Resources
- **Stack Overflow:** Tag `google-ads-api`
- **Google Ads API Forum:** https://groups.google.com/g/adwords-api
- **GitHub Issues:** For MCP server-specific issues

### Getting Help
1. Check documentation first
2. Search Stack Overflow
3. Review GitHub issues
4. Post in Google Ads API forum
5. Contact Google Ads API support (for API-specific issues)

---

**Last Updated:** 2025-12-16
**Version:** 1.0
**Status:** Complete Setup Guide


