"""Shared fixtures for ByCrawl tests."""

from __future__ import annotations

import httpx
import pytest
import respx

from bycrawl import AsyncByCrawl, ByCrawl


@pytest.fixture()
def mock_api():
    """RESPX mock router scoped to each test."""
    with respx.mock(base_url="https://api.bycrawl.com", assert_all_called=False) as router:
        yield router


@pytest.fixture()
def client(mock_api: respx.Router) -> ByCrawl:
    """Sync ByCrawl client wired to the mock."""
    return ByCrawl(api_key="sk_byc_test")


@pytest.fixture()
def async_client(mock_api: respx.Router) -> AsyncByCrawl:
    """Async ByCrawl client wired to the mock."""
    return AsyncByCrawl(api_key="sk_byc_test")


def make_response(
    data: object = None,
    *,
    status_code: int = 200,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Helper to build a mock httpx.Response with standard ByCrawl JSON envelope."""
    body = {"data": data} if data is not None else {}
    all_headers = {
        "content-type": "application/json",
        **(headers or {}),
    }
    return httpx.Response(status_code, json=body, headers=all_headers)
