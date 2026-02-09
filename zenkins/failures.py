"""zenkins failures <job> [build] - show failing tests."""

import argparse

from zenkins.client import api_get, job_path


def failures_command(args: argparse.Namespace) -> None:
    """Show failing tests for a build (JUnit + Robot Framework)."""
    job = args.job
    build = args.build or "lastBuild"
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
