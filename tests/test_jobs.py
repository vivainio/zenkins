"""Tests for zenkins.jobs."""

import argparse
from unittest.mock import MagicMock, patch

from zenkins.jobs import jobs_command, STATUS_MAP, COLOR_MAP


def test_jobs_command(mock_session, capsys):
    """Test jobs listing."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "jobs": [
            {"name": "my-job", "color": "blue", "url": "http://j/job/my-job/"},
            {"name": "broken-job", "color": "red", "url": "http://j/job/broken-job/"},
        ]
    }
    mock_session.get.return_value = mock_resp

    with patch("zenkins.client.get_base_url", return_value="http://j"):
        jobs_command(argparse.Namespace())

    out = capsys.readouterr().out
    assert "my-job" in out
    assert "broken-job" in out
    assert "SUCCESS" in out
    assert "FAILURE" in out


def test_jobs_empty(mock_session, capsys):
    """Test empty jobs list."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"jobs": []}
    mock_session.get.return_value = mock_resp

    with patch("zenkins.client.get_base_url", return_value="http://j"):
        jobs_command(argparse.Namespace())

    out = capsys.readouterr().out
    assert "No jobs found" in out


def test_status_map_covers_colors():
    """All colors in COLOR_MAP should have a STATUS_MAP entry."""
    for color in COLOR_MAP:
        assert color in STATUS_MAP
