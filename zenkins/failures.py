"""zenkins failures <job> [build] - show failing tests."""

import argparse
from collections import Counter

from zenkins.client import api_get, job_path


def _get_failures(job: str, build: str) -> list[str]:
    """Get all failing test names for a single build."""
    base = f"{job_path(job)}/{build}"
    failures = []

    # JUnit / NUnit
    try:
        resp = api_get(f"{base}/testReport/api/json?tree=suites[cases[name,className,status]]")
        data = resp.json()
        for suite in data.get("suites", []):
            for case in suite.get("cases", []):
                if case["status"] not in ("PASSED", "SKIPPED", "FIXED"):
                    failures.append(f"{case['className']}.{case['name']}")
    except Exception:
        pass

    # Robot Framework
    try:
        resp = api_get(f"{base}/robot/api/json?tree=failedCases")
        data = resp.json()
        failures.extend(data.get("failedCases", []))
    except Exception:
        pass

    return failures


def _parse_build_range(build_spec: str) -> tuple[int, int] | None:
    """Parse 'N..M' into (N, M) or return None."""
    if ".." not in build_spec:
        return None
    parts = build_spec.split("..", 1)
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def _single_build(job: str, build: str) -> None:
    """Show failures for a single build."""
    base = f"{job_path(job)}/{build}"
    found = False

    # JUnit / NUnit test report
    try:
        resp = api_get(f"{base}/testReport/api/json?tree=failCount,passCount,skipCount,suites[cases[name,className,status,errorDetails]]")
        data = resp.json()
        fail_count = data.get("failCount", 0)
        pass_count = data.get("passCount", 0)
        if fail_count:
            print(f"JUnit: {fail_count} failed, {pass_count} passed\n")
            for suite in data.get("suites", []):
                for case in suite.get("cases", []):
                    if case["status"] not in ("PASSED", "SKIPPED", "FIXED"):
                        print(f"  FAIL: {case['className']}.{case['name']}")
                        if case.get("errorDetails"):
                            for line in case["errorDetails"].splitlines()[:3]:
                                print(f"        {line}")
                            print()
            found = True
        elif pass_count:
            print(f"JUnit: all {pass_count} passed")
            found = True
    except Exception:
        pass

    # Robot Framework
    try:
        resp = api_get(f"{base}/robot/api/json?tree=overallFailed,overallPassed,failedCases")
        data = resp.json()
        failed = data.get("overallFailed", 0)
        passed = data.get("overallPassed", 0)
        if failed:
            print(f"Robot: {failed} failed, {passed} passed\n")
            for case in data.get("failedCases", []):
                print(f"  FAIL: {case}")
            print()
            found = True
        elif passed:
            print(f"Robot: all {passed} passed")
            found = True
    except Exception:
        pass

    if not found:
        print("No test results found for this build.")


def _range_builds(job: str, start: int, end: int) -> None:
    """Show failure summary across a range of builds."""
    builds = list(range(start, end + 1))
    total = len(builds)
    counts: Counter[str] = Counter()
    build_failures: dict[str, list[int]] = {}

    for b in builds:
        print(f"\r  Fetching build #{b}...", end="", flush=True)
        failures = _get_failures(job, str(b))
        for f in failures:
            counts[f] += 1
            build_failures.setdefault(f, []).append(b)

    print(f"\r{total} builds, #{start}-#{end}                    \n")

    if not counts:
        print("No test failures found.")
        return

    persistent = [(name, c) for name, c in counts.items() if c == total]
    intermittent = [(name, c) for name, c in counts.items() if 1 < c < total]
    oneoff = [(name, c) for name, c in counts.items() if c == 1]

    if persistent:
        print(f"Persistent ({total}/{total} builds):")
        for name, _ in sorted(persistent):
            print(f"  {name}")
        print()

    if intermittent:
        print("Intermittent:")
        for name, c in sorted(intermittent, key=lambda x: -x[1]):
            print(f"  {name} ({c}/{total})")
        print()

    if oneoff:
        print("One-off:")
        for name, _ in sorted(oneoff):
            builds_str = ", ".join(f"#{b}" for b in build_failures[name])
            print(f"  {name} ({builds_str})")
        print()


def failures_command(args: argparse.Namespace) -> None:
    """Show failing tests for a build or range of builds."""
    job = args.job
    build = args.build or "lastBuild"

    rng = _parse_build_range(build)
    if rng:
        _range_builds(job, rng[0], rng[1])
    else:
        _single_build(job, build)
