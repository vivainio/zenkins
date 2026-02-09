"""zenkins init - verify Jenkins configuration."""

import argparse
import sys

from zenkins.client import CONFIG_FILE, _LEGACY_CONFIG, load_credentials, api_get


def init_command(args: argparse.Namespace) -> None:
    """Verify Jenkins credentials and connectivity."""
    print(f"Config file: {CONFIG_FILE}")

    if not CONFIG_FILE.exists() and not _LEGACY_CONFIG.exists():
        print(f"\nError: Config file not found at {CONFIG_FILE}", file=sys.stderr)
        print("Create it with:", file=sys.stderr)
        print('  url = "http://your-jenkins.example.com"', file=sys.stderr)
        print('  user = "your-username"', file=sys.stderr)
        print('  token = "your-api-token"', file=sys.stderr)
        sys.exit(1)

    creds = load_credentials()
    url = creds.get("url", "")
    user = creds.get("user", "")
    token = creds.get("token", "")

    print(f"URL:  {url}")
    print(f"User: {user}")
    print(f"Token: {'*' * 8}...{token[-4:]}" if len(token) > 4 else f"Token: {'*' * len(token)}")

    # Test connectivity
    print("\nTesting connection...")
    try:
        resp = api_get("/api/json?tree=mode,nodeDescription,useSecurity")
        data = resp.json()
        print(f"Connected: {data.get('nodeDescription', 'Jenkins')}")
        print(f"Security:  {'enabled' if data.get('useSecurity') else 'disabled'}")
    except Exception as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        sys.exit(1)
