"""zenkins artifacts <job> [build] [-d DIR] [--glob PATTERN] - download build artifacts."""

import argparse
from pathlib import Path

from zenkins.client import api_get, get_base_url, get_session, job_path


def artifacts_command(args: argparse.Namespace) -> None:
    """List or download artifacts for a build."""
    job = args.job
    build = args.build or "lastBuild"
    dest = Path(args.dir)
    pattern = args.glob

    resp = api_get(
        f"{job_path(job)}/{build}/api/json?tree=artifacts[relativePath]"
    )
    data = resp.json()
    artifacts = data.get("artifacts", [])

    if not artifacts:
        print(f"No artifacts for {job} #{build}")
        return

    if pattern:
        from fnmatch import fnmatch

        artifacts = [a for a in artifacts if fnmatch(a["relativePath"], pattern)]
        if not artifacts:
            print(f"No artifacts matching '{pattern}'")
            return

    if args.list:
        for a in artifacts:
            print(a["relativePath"])
        return

    dest.mkdir(parents=True, exist_ok=True)
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

    print(f"\n{len(artifacts)} artifact(s) downloaded to {dest}")
