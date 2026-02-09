"""Zenkins CLI - Main entry point."""

import argparse
import sys

from zenkins import __version__
from zenkins.artifacts import artifacts_command
from zenkins.build import build_command
from zenkins.builds import builds_command
from zenkins.failures import failures_command
from zenkins.init import init_command
from zenkins.jobs import jobs_command
from zenkins.log import log_command
from zenkins.queue import queue_command
from zenkins.status import status_command


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="zenkins",
        description="Jenkins CLI tool",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init
    subparsers.add_parser("init", help="Verify Jenkins configuration and connectivity")

    # jobs
    subparsers.add_parser("jobs", help="List all jobs with status")

    # status
    status_parser = subparsers.add_parser("status", help="Show last build info for a job")
    status_parser.add_argument("job", help="Job name")

    # builds
    builds_parser = subparsers.add_parser("builds", help="List recent builds for a job")
    builds_parser.add_argument("job", help="Job name")
    builds_parser.add_argument("-n", type=int, default=10, help="Number of builds (default: 10)")

    # log
    log_parser = subparsers.add_parser("log", help="Show console output for a build")
    log_parser.add_argument("job", help="Job name")
    log_parser.add_argument("build", nargs="?", help="Build number (default: last build)")

    # queue
    subparsers.add_parser("queue", help="Show build queue")

    # failures
    failures_parser = subparsers.add_parser("failures", help="Show failing tests for a build")
    failures_parser.add_argument("job", help="Job name")
    failures_parser.add_argument("build", nargs="?", help="Build number or range (e.g. 42, 40..45)")
    failures_parser.add_argument("-n", type=int, help="Summarize last N builds")

    # artifacts
    artifacts_parser = subparsers.add_parser("artifacts", help="List or download build artifacts")
    artifacts_parser.add_argument("job", help="Job name")
    artifacts_parser.add_argument("build", nargs="?", help="Build number or range (e.g. 42, 40..45)")
    artifacts_parser.add_argument("-n", type=int, help="Fetch last N builds")
    artifacts_parser.add_argument("-d", "--dir", default=".", help="Download directory (default: .)")
    artifacts_parser.add_argument("--glob", help="Filter artifacts by glob pattern")
    artifacts_parser.add_argument("-l", "--list", action="store_true", help="List artifacts without downloading")

    # build
    build_parser = subparsers.add_parser("build", help="Trigger a build")
    build_parser.add_argument("job", help="Job name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "artifacts": artifacts_command,
        "failures": failures_command,
        "init": init_command,
        "jobs": jobs_command,
        "status": status_command,
        "builds": builds_command,
        "log": log_command,
        "queue": queue_command,
        "build": build_command,
    }

    commands[args.command](args)
