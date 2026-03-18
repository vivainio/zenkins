"""zenkins build <job> - trigger a build."""

import argparse

from zenkins.client import api_post, job_path

GREEN = "\033[32m"
RESET = "\033[0m"


def build_command(args: argparse.Namespace) -> None:
    """Trigger a build for a job, optionally with parameters."""
    job = args.job
    params = {}
    for item in args.param or []:
        key, _, value = item.partition("=")
        if not _:
            raise SystemExit(f"Invalid parameter format: {item!r} (expected KEY=VALUE)")
        params[key] = value

    if params:
        api_post(f"{job_path(job)}/buildWithParameters", params=params)
        param_str = ", ".join(f"{k}={v}" for k, v in params.items())
        print(f"{GREEN}Build triggered:{RESET} {job}  [{param_str}]")
    else:
        api_post(f"{job_path(job)}/build")
        print(f"{GREEN}Build triggered:{RESET} {job}")
