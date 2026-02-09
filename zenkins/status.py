"""zenkins status <job> - last build info."""

import argparse
from datetime import datetime, timezone

from zenkins.client import api_get, job_path

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

RESULT_COLORS = {
    "SUCCESS": GREEN,
    "FAILURE": RED,
    "UNSTABLE": YELLOW,
    "ABORTED": GRAY,
    None: YELLOW,
}


def format_duration(ms: int) -> str:
    """Format milliseconds to human-readable duration."""
    seconds = ms // 1000
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"


def format_timestamp(ts: int) -> str:
    """Format Unix millisecond timestamp."""
    dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).astimezone()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def status_command(args: argparse.Namespace) -> None:
    """Show status of the last build for a job."""
    job = args.job
    tree = "lastBuild[number,result,timestamp,duration,building,displayName,description]"
    resp = api_get(f"{job_path(job)}/api/json?tree={tree}")
    data = resp.json()

    build = data.get("lastBuild")
    if not build:
        print(f"No builds found for {job}")
        return

    result = build.get("result")
    building = build.get("building", False)
    color = RESULT_COLORS.get(result, GRAY)

    if building:
        status_str = f"{YELLOW}BUILDING{RESET}"
    elif result:
        status_str = f"{color}{result}{RESET}"
    else:
        status_str = f"{GRAY}UNKNOWN{RESET}"

    print(f"{BOLD}{job}{RESET}  #{build['number']}")
    print(f"  Status:   {status_str}")
    print(f"  Started:  {format_timestamp(build['timestamp'])}")
    print(f"  Duration: {format_duration(build['duration'])}")

    if build.get("description"):
        print(f"  Desc:     {build['description']}")
