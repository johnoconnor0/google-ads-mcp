"""Generate a Google Ads OAuth refresh token for local MCP setup."""

from __future__ import annotations

import json
import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]


def _load_client_config() -> dict:
    credentials_path = Path("credentials.json")
    if credentials_path.exists():
        return json.loads(credentials_path.read_text(encoding="utf-8"))

    client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "Provide credentials.json or set GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET"
        )

    return {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }


def main() -> None:
    client_config = _load_client_config()
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)

    print("Refresh token generated successfully.")
    print(f"GOOGLE_ADS_REFRESH_TOKEN={creds.refresh_token}")


if __name__ == "__main__":
    main()
