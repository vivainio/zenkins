"""zenkins init - verify Jenkins configuration."""

import argparse
import sys

from zenkins.client import CONFIG_FILE, load_credentials, api_get, _active_profile


def init_command(args: argparse.Namespace) -> None:
    """Verify Jenkins credentials and connectivity."""
    profile = _active_profile
    print(f"Config file: {CONFIG_FILE}")
    if profile:
        print(f"Profile:     {profile}")

    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(
            'url = "http://your-jenkins.example.com"\n'
            'user = "your-username"\n'
            'token = "your-api-token"\n'
            '\n# Example named profile:\n'
            '# [profile.deployment]\n'
            '# url = "https://deployment-jenkins.example.com"\n'
            '# user = "your-username"\n'
            '# token = "your-api-token"\n'
        )
        print(f"Created config file with defaults — edit it and run init again.")
        print("To create an API token: Jenkins → Your name (top right) → Configure → API Token → Add new Token")
        sys.exit(0)

    creds = load_credentials(profile)
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
