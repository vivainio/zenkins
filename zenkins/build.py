"""zenkins build <job> - trigger a build."""

import argparse

from zenkins.client import api_post

GREEN = "\033[32m"
RESET = "\033[0m"


def build_command(args: argparse.Namespace) -> None:
    """Trigger a build for a job."""
    job = args.job
    api_post(f"/job/{job}/build")
    print(f"{GREEN}Build triggered:{RESET} {job}")
