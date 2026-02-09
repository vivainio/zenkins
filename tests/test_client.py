"""Tests for zenkins.client."""

from unittest.mock import MagicMock, patch
from pathlib import Path

from zenkins.client import load_credentials, api_get, api_post


def test_load_credentials(tmp_path):
    """Test loading KEY=VALUE config file."""
    config = tmp_path / "config"
    config.write_text(
        "JENKINS_URL=http://jenkins.example.com\n"
        "JENKINS_USER=testuser\n"
        "JENKINS_TOKEN=abc123\n"
    )

    with patch("zenkins.client.CONFIG_FILE", config):
        creds = load_credentials()

    assert creds["url"] == "http://jenkins.example.com"
    assert creds["user"] == "testuser"
    assert creds["token"] == "abc123"


def test_load_credentials_missing_file(tmp_path):
    """Test loading from nonexistent file returns empty dict."""
    config = tmp_path / "nonexistent"

    with patch("zenkins.client.CONFIG_FILE", config):
        creds = load_credentials()

    assert creds == {}


def test_load_credentials_comments_and_blanks(tmp_path):
    """Test that comments and blank lines are ignored."""
    config = tmp_path / "config"
    config.write_text(
        "# This is a comment\n"
        "\n"
        "JENKINS_URL=http://jenkins.example.com\n"
        "  \n"
        "JENKINS_USER=testuser\n"
    )

    with patch("zenkins.client.CONFIG_FILE", config):
        creds = load_credentials()

    assert creds["url"] == "http://jenkins.example.com"
    assert creds["user"] == "testuser"
    assert "token" not in creds


def test_api_get(mock_session):
    """Test api_get combines base URL and path."""
    mock_resp = MagicMock()
    mock_session.get.return_value = mock_resp

    with patch("zenkins.client.get_base_url", return_value="http://jenkins.example.com"):
        resp = api_get("/api/json")

    mock_session.get.assert_called_once_with("http://jenkins.example.com/api/json")
    mock_resp.raise_for_status.assert_called_once()


def test_api_post(mock_session):
    """Test api_post combines base URL and path."""
    mock_resp = MagicMock()
    mock_session.post.return_value = mock_resp

    with patch("zenkins.client.get_base_url", return_value="http://jenkins.example.com"):
        resp = api_post("/job/test/build")

    mock_session.post.assert_called_once_with("http://jenkins.example.com/job/test/build")
    mock_resp.raise_for_status.assert_called_once()
