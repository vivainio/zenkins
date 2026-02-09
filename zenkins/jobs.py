"""zenkins jobs - list all jobs with status."""

import argparse

from zenkins.client import api_get

# ANSI colors
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

COLOR_MAP = {
    "blue": GREEN,           # success
    "blue_anime": GREEN,     # success + building
    "red": RED,              # failure
    "red_anime": RED,        # failure + building
    "yellow": YELLOW,        # unstable
    "yellow_anime": YELLOW,  # unstable + building
    "aborted": GRAY,
    "aborted_anime": GRAY,
    "disabled": GRAY,
    "notbuilt": GRAY,
    "notbuilt_anime": GRAY,
}

STATUS_MAP = {
    "blue": "SUCCESS",
    "blue_anime": "BUILDING",
    "red": "FAILURE",
    "red_anime": "BUILDING",
    "yellow": "UNSTABLE",
    "yellow_anime": "BUILDING",
    "aborted": "ABORTED",
    "aborted_anime": "BUILDING",
    "disabled": "DISABLED",
    "notbuilt": "NOT BUILT",
    "notbuilt_anime": "BUILDING",
}


def jobs_command(args: argparse.Namespace) -> None:
    """List all jobs with their current status."""
    tree = "jobs[name,color,url]"
    resp = api_get(f"/api/json?tree={tree}")
    data = resp.json()
    jobs = data.get("jobs", [])

    if not jobs:
        print("No jobs found.")
        return

    # Calculate column width
    max_name = max(len(j["name"]) for j in jobs)

    for job in sorted(jobs, key=lambda j: j["name"]):
        color_code = job.get("color", "notbuilt")
        ansi = COLOR_MAP.get(color_code, GRAY)
        status = STATUS_MAP.get(color_code, color_code)
        building = " *" if "_anime" in (color_code or "") else ""

        name = job["name"].ljust(max_name)
        print(f"  {ansi}{status:>10}{RESET}  {name}{building}")
