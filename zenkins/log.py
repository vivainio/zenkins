"""zenkins log <job> [build] - console output."""

import argparse

from zenkins.client import api_get, job_path


def log_command(args: argparse.Namespace) -> None:
    """Show console output for a build."""
    job = args.job
    build = args.build or "lastBuild"

    resp = api_get(f"{job_path(job)}/{build}/consoleText")
    print(resp.text)
