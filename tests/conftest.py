"""Shared pytest fixtures for zenkins tests."""

import pytest
from unittest.mock import MagicMock

from zenkins.client import set_session, reset_session


@pytest.fixture
def mock_session():
    """Provide a mock requests session.

    The mock is injected into client module and automatically reset after the test.

    Usage:
        def test_something(mock_session):
            mock_session.get.return_value = MockResponse(...)
            # Test code that calls client.api_get()
    """
    mock = MagicMock()
    set_session(mock)
    yield mock
    reset_session()
