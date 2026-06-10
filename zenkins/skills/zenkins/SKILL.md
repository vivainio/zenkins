---
name: zenkins
description: CLI for Jenkins. Use when checking build status, viewing logs, investigating failures, downloading artifacts, or triggering builds. Triggers when user mentions "jenkins", "build status", "build log", "build failures", or asks about CI job results.
---

# zenkins CLI

`zenkins` is a CLI tool for interacting with a Jenkins server. Configure the server URL and credentials with `zenkins init`.

## Commands

### List all jobs
```bash
zenkins jobs                 # top-level jobs
zenkins jobs <folder>        # jobs inside a folder
```

### Last build status for a job
```bash
zenkins status <job>
```

### Recent builds
```bash
zenkins builds <job>         # last 10
zenkins builds -n 20 <job>   # last 20
```

### Console log
```bash
zenkins log <job>            # last build
zenkins log <job> 142        # specific build
```

### Build queue
```bash
zenkins queue
```

### Failing tests
```bash
zenkins failures <job>             # last build
zenkins failures <job> 142         # specific build
zenkins failures <job> 140..145    # build range
zenkins failures -n 5 <job>        # summarize last 5 builds
```

### Artifacts
```bash
zenkins artifacts -l <job>                    # list artifacts (last build)
zenkins artifacts -l <job> 142                # list for specific build
zenkins artifacts <job> -d ./out              # download to directory
zenkins artifacts <job> --glob "*.log"        # filter by pattern
zenkins artifacts -n 3 <job>                  # last 3 builds
```

### List build parameters
```bash
zenkins params <job>
```

### Trigger a build
```bash
zenkins build <job>                              # simple build
zenkins build <job> -p KEY=VALUE -p KEY2=VALUE2  # with parameters
```

### Verify connection
```bash
zenkins init
```

## Tips

- Some top-level entries are **folders** containing nested jobs/branches. Use `zenkins jobs <folder>` to list contents, and `folder/job` syntax for other commands (e.g. `zenkins status folder/job`).
- Job names are case-sensitive and match exactly as shown in `zenkins jobs`.
- Build ranges use `..` syntax: `140..145`.
- Use `failures -n N` to get a trend of test failures across recent builds.
- Pipe output to `grep` or `less` for large logs: `zenkins log <job> | less`.
