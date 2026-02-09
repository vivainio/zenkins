"""Jenkins HTTP client - session management and credential loading."""

import sys
from functools import lru_cache
from pathlib import Path

import platformdirs
import requests

from zenkins.types import Credentials

CONFIG_FILE = Path(platformdirs.user_config_dir("zenkins")) / "config"


def job_path(job: str) -> str:
    """Convert a job name like 'p2p/dev' to '/job/p2p/job/dev'."""
    return "/job/" + "/job/".join(job.split("/"))


def load_credentials() -> Credentials:
    """Load credentials from ~/.config/jenkins/config (KEY=VALUE format)."""
    if not CONFIG_FILE.exists():
        return {}

    creds: Credentials = {}
    for line in CONFIG_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key == "JENKINS_URL":
            creds["url"] = value
        elif key == "JENKINS_USER":
            creds["user"] = value
        elif key == "JENKINS_TOKEN":
            creds["token"] = value
    return creds


def get_credentials() -> tuple[str, str, str]:
    """Get Jenkins credentials.

    Returns:
        Tuple of (url, user, token)
    """
    creds = load_credentials()
    url = creds.get("url")
    user = creds.get("user")
    token = creds.get("token")

    if not url or not user or not token:
        print(f"Error: Credentials not configured in {CONFIG_FILE}", file=sys.stderr)
        print("\nRun 'zenkins init' to check configuration.", file=sys.stderr)
        sys.exit(1)

    return url.rstrip("/"), user, token


# Injected session for testing
_session: requests.Session | None = None


def get_session() -> requests.Session:
    """Get the requests session (cached or injected)."""
    global _session
    if _session is not None:
        return _session
    return _get_default_session()


@lru_cache(maxsize=1)
def _get_default_session() -> requests.Session:
    """Create the default authenticated session."""
    url, user, token = get_credentials()
    s = requests.Session()
    s.auth = (user, token)
    return s


def set_session(session: requests.Session | None) -> None:
    """Inject a session for testing. Pass None to reset."""
    global _session
    _session = session


def reset_session() -> None:
    """Reset to default session and clear cache."""
    global _session
    _session = None
    _get_default_session.cache_clear()


def get_base_url() -> str:
    """Get the Jenkins base URL."""
    url, _, _ = get_credentials()
    return url


def api_get(path: str, **kwargs) -> requests.Response:
    """GET a Jenkins API path.

    Args:
        path: API path (e.g., "/api/json" or "/job/foo/api/json")
        **kwargs: Extra arguments passed to session.get()

    Returns:
        Response object
    """
    url = get_base_url() + path
    resp = get_session().get(url, **kwargs)
    resp.raise_for_status()
    return resp


def api_post(path: str, **kwargs) -> requests.Response:
    """POST to a Jenkins API path.

    Args:
        path: API path (e.g., "/job/foo/build")
        **kwargs: Extra arguments passed to session.post()

    Returns:
        Response object
    """
    url = get_base_url() + path
    resp = get_session().post(url, **kwargs)
    resp.raise_for_status()
    return resp
