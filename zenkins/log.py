"""zenkins log <job> [build] - console output."""

import argparse

from zenkins.client import api_get


def log_command(args: argparse.Namespace) -> None:
    """Show console output for a build."""
    job = args.job
    build = args.build or "lastBuild"

    resp = api_get(f"/job/{job}/{build}/consoleText")
    print(resp.text)
