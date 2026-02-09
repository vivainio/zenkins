# zenkins

CLI tool for Jenkins. List jobs, check builds, view logs, trigger builds.

## Install

```bash
uv tool install zenkins
```

## Setup

Run `zenkins init` to configure your Jenkins connection. This creates `~/.config/zenkins/config` with your Jenkins URL and credentials.

## Usage

```bash
zenkins jobs                        # List all jobs with status
zenkins status <job>                # Show last build info
zenkins builds <job>                # List recent builds
zenkins builds <job> -n 5           # List last 5 builds
zenkins log <job>                   # Show console output (last build)
zenkins log <job> 42                # Show console output for build #42
zenkins queue                       # Show build queue
zenkins build <job>                 # Trigger a build
zenkins failures <job>              # Show failing tests (last build)
zenkins failures <job> 42           # Show failing tests for build #42
zenkins failures <job> 40..45       # Failure summary across build range
zenkins failures <job> -n 10        # Failure summary for last 10 builds
zenkins artifacts <job> -l          # List artifacts (last build)
zenkins artifacts <job> 42 -d ./out # Download artifacts to directory
zenkins artifacts <job> --glob "*.xml" # Download matching artifacts
zenkins artifacts <job> -n 3 --glob "*.png" -l  # List PNGs from last 3 builds
```

Folder jobs use `/` syntax: `zenkins builds ci/main`, `zenkins failures ci/main -n 5`.

The `failures` command queries both JUnit/NUnit and Robot Framework test results,
grouping them into persistent, intermittent, and one-off failures when using
range or `-n` syntax.

## Library usage

```python
import zenkins

s = zenkins.client()
resp = s.get("http://jenkins.example.com/api/json")
```

## License

MIT
