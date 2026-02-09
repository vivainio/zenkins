"""Type definitions for Jenkins API responses."""

from typing import TypedDict


class HealthReport(TypedDict, total=False):
    description: str
    score: int


class Job(TypedDict, total=False):
    name: str
    url: str
    color: str
    healthReport: list[HealthReport]
    lastBuild: "Build | None"
    lastSuccessfulBuild: "Build | None"
    lastFailedBuild: "Build | None"
    inQueue: bool


class Build(TypedDict, total=False):
    number: int
    url: str
    result: str | None
    timestamp: int
    duration: int
    building: bool
    displayName: str
    description: str | None
    fullDisplayName: str


class QueueItem(TypedDict, total=False):
    id: int
    task: Job
    why: str | None
    stuck: bool
    buildable: bool
    blocked: bool


class Credentials(TypedDict, total=False):
    url: str
    user: str
    token: str
