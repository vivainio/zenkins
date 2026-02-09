"""Zenkins - Jenkins CLI tool."""

from importlib.metadata import version

__version__ = version("zenkins")


def client() -> "requests.Session":
    """Get an authenticated Jenkins session.

    Returns a requests.Session configured with Jenkins credentials
    from ~/.config/jenkins/config.

    Usage:
        import zenkins
        s = zenkins.client()
        resp = s.get("http://jenkins.example.com/api/json")

    Returns:
        requests.Session: Authenticated session
    """
    from zenkins.client import get_session

    return get_session()
