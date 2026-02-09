# zenkins

CLI tool for Jenkins. List jobs, check builds, view logs, trigger builds.

## Install

```bash
pip install zenkins
```

## Setup

Run `zenkins init` to configure your Jenkins connection. This creates `~/.config/jenkins/config` with your Jenkins URL and credentials.

## Usage

```bash
zenkins jobs              # List all jobs with status
zenkins status <job>      # Show last build info
zenkins builds <job>      # List recent builds
zenkins builds <job> -n 5 # List last 5 builds
zenkins log <job>         # Show console output (last build)
zenkins log <job> 42      # Show console output for build #42
zenkins queue             # Show build queue
zenkins build <job>       # Trigger a build
```

## Library usage

```python
import zenkins

s = zenkins.client()
resp = s.get("http://jenkins.example.com/api/json")
```

## License

MIT
