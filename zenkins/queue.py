"""zenkins queue - build queue."""

import argparse

from zenkins.client import api_get

YELLOW = "\033[33m"
RED = "\033[31m"
GRAY = "\033[90m"
RESET = "\033[0m"


def queue_command(args: argparse.Namespace) -> None:
    """Show the Jenkins build queue."""
    resp = api_get("/queue/api/json?tree=items[id,task[name],why,stuck,blocked,buildable]")
    data = resp.json()

    items = data.get("items", [])
    if not items:
        print("Build queue is empty.")
        return

    print(f"Queue: {len(items)} item(s)\n")
    for item in items:
        task_name = item.get("task", {}).get("name", "?")
        why = item.get("why", "")
        stuck = item.get("stuck", False)

        if stuck:
            color = RED
            flag = " [STUCK]"
        else:
            color = YELLOW
            flag = ""

        print(f"  {color}{task_name}{RESET}{flag}")
        if why:
            print(f"    {GRAY}{why}{RESET}")
