"""zenkins build <job> - trigger a build."""

import argparse

from zenkins.client import api_post, job_path

GREEN = "\033[32m"
RESET = "\033[0m"


def build_command(args: argparse.Namespace) -> None:
    """Trigger a build for a job."""
    job = args.job
    api_post(f"{job_path(job)}/build")
    print(f"{GREEN}Build triggered:{RESET} {job}")
