"""zenkins params <job> - list build parameters for a job."""

import argparse

from zenkins.client import api_get, job_path

BOLD = "\033[1m"
GRAY = "\033[90m"
RESET = "\033[0m"

# Separator types are visual-only in the Jenkins UI, not real parameters
SEPARATOR_TYPES = {"ParameterSeparatorDefinition"}


def params_command(args: argparse.Namespace) -> None:
    """List build parameters for a job."""
    job = args.job
    tree = "property[parameterDefinitions[name,type,description,defaultParameterValue[value],choices]]"
    resp = api_get(f"{job_path(job)}/api/json?tree={tree}")
    data = resp.json()

    params = []
    for prop in data.get("property", []):
        for p in prop.get("parameterDefinitions", []):
            if p.get("type") not in SEPARATOR_TYPES:
                params.append(p)

    if not params:
        print("No parameters defined for this job.")
        return

    for p in params:
        name = p.get("name", "")
        ptype = p.get("type", "").replace("ParameterDefinition", "").replace("ParameterValue", "")
        default = p.get("defaultParameterValue", {}).get("value")
        desc = p.get("description", "") or ""
        choices = p.get("choices")

        default_str = ""
        if default is not None and default != "":
            default_str = f"  {GRAY}default: {default}{RESET}"

        print(f"  {BOLD}{name}{RESET}  ({ptype}){default_str}")
        if desc:
            print(f"    {desc}")
        if choices:
            print(f"    choices: {', '.join(choices)}")
