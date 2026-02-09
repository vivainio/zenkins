"""zenkins builds <job> [-n N] - recent builds."""

import argparse
from datetime import datetime, timezone

from zenkins.client import api_get

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
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


def builds_command(args: argparse.Namespace) -> None:
    """List recent builds for a job."""
    job = args.job
    n = args.n
    tree = f"builds[number,result,timestamp,duration,building]{{{0},{n}}}"
    resp = api_get(f"/job/{job}/api/json?tree={tree}")
    data = resp.json()

    builds = data.get("builds", [])
    if not builds:
        print(f"No builds found for {job}")
        return

    for build in builds:
        number = build["number"]
        result = build.get("result")
        building = build.get("building", False)
        ts = build.get("timestamp", 0)
        dur = build.get("duration", 0)

        dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).astimezone()
        date_str = dt.strftime("%Y-%m-%d %H:%M")
        dur_str = format_duration(dur)

        if building:
            color = YELLOW
            status = "BUILDING"
        elif result:
            color = RESULT_COLORS.get(result, GRAY)
            status = result
        else:
            color = GRAY
            status = "?"

        print(f"  #{number:<6} {color}{status:>10}{RESET}  {date_str}  {dur_str}")
