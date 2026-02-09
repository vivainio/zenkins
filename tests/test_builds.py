"""Tests for zenkins.builds and zenkins.status."""

import argparse
from unittest.mock import MagicMock, patch

from zenkins.builds import builds_command, format_duration
from zenkins.status import status_command, format_timestamp


def test_format_duration_seconds():
    assert format_duration(5000) == "5s"


def test_format_duration_minutes():
    assert format_duration(125000) == "2m 5s"


def test_format_duration_hours():
    assert format_duration(3725000) == "1h 2m"


def test_format_timestamp():
    ts = format_timestamp(1700000000000)
    # Exact date depends on timezone, just check format
    assert "2023-11-1" in ts
    assert ":" in ts


def test_builds_command(mock_session, capsys):
    """Test builds listing."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "builds": [
            {
                "number": 42,
                "result": "SUCCESS",
                "timestamp": 1700000000000,
                "duration": 60000,
                "building": False,
            },
            {
                "number": 41,
                "result": "FAILURE",
                "timestamp": 1699990000000,
                "duration": 30000,
                "building": False,
            },
        ]
    }
    mock_session.get.return_value = mock_resp

    args = argparse.Namespace(job="test-job", n=10)
    with patch("zenkins.client.get_base_url", return_value="http://j"):
        builds_command(args)

    out = capsys.readouterr().out
    assert "#42" in out
    assert "#41" in out
    assert "SUCCESS" in out
    assert "FAILURE" in out


def test_status_command(mock_session, capsys):
    """Test status display."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "lastBuild": {
            "number": 99,
            "result": "SUCCESS",
            "timestamp": 1700000000000,
            "duration": 120000,
            "building": False,
            "displayName": "#99",
            "description": None,
        }
    }
    mock_session.get.return_value = mock_resp

    args = argparse.Namespace(job="my-job")
    with patch("zenkins.client.get_base_url", return_value="http://j"):
        status_command(args)

    out = capsys.readouterr().out
    assert "my-job" in out
    assert "#99" in out
    assert "SUCCESS" in out
