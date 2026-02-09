"""zenkins artifacts <job> [build] [-d DIR] [--glob PATTERN] - download build artifacts."""

import argparse
from fnmatch import fnmatch
from pathlib import Path

from zenkins.client import api_get, get_base_url, get_session, job_path
from zenkins.failures import _resolve_builds


def _get_artifacts(job: str, build: str, pattern: str | None) -> list[str]:
    """Get artifact paths for a build, optionally filtered by glob."""
    resp = api_get(
        f"{job_path(job)}/{build}/api/json?tree=artifacts[relativePath]"
    )
    artifacts = resp.json().get("artifacts", [])
    if pattern:
        artifacts = [a for a in artifacts if fnmatch(a["relativePath"], pattern)]
    return artifacts


def _download_artifacts(
    job: str, build: str, artifacts: list[dict], dest: Path,
) -> int:
    """Download artifacts for a single build. Returns count."""
    base = get_base_url()
    session = get_session()
    for a in artifacts:
        rel = a["relativePath"]
        url = f"{base}{job_path(job)}/{build}/artifact/{rel}"
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        resp = session.get(url)
        resp.raise_for_status()
        out.write_bytes(resp.content)
        print(f"  {out}")
    return len(artifacts)


def artifacts_command(args: argparse.Namespace) -> None:
    """List or download artifacts for one or more builds."""
    job = args.job
    dest = Path(args.dir)
    pattern = args.glob

    multi_builds = _resolve_builds(job, args.build, args.n)
    builds = multi_builds if multi_builds else [args.build or "lastBuild"]
    multi = multi_builds is not None

    total = 0
    for build in builds:
        artifacts = _get_artifacts(job, build, pattern)
        if not artifacts:
            if not multi:
                print(f"No artifacts for {job} #{build}")
            continue

        if args.list:
            if multi:
                for a in artifacts:
                    print(f"{build}/{a['relativePath']}")
            else:
                for a in artifacts:
                    print(a["relativePath"])
        else:
            build_dest = dest / build if multi else dest
            total += _download_artifacts(job, build, artifacts, build_dest)

    if not args.list and total:
        print(f"\n{total} artifact(s) downloaded to {dest}")
