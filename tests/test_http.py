"""Tests for HTTP transport layer."""

from __future__ import annotations

import httpx
import pytest
import respx

from bycrawl import (
    AuthenticationError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
)
from bycrawl._exceptions import APIError
from bycrawl._http import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    SDK_VERSION,
    ResponseWrapper,
    SyncTransport,
    _backoff_delay,
    _make_headers,
    _raise_for_status,
    _user_agent,
)


class TestConstants:
    def test_default_base_url(self):
        assert DEFAULT_BASE_URL == "https://api.bycrawl.com"

    def test_default_timeout(self):
        assert DEFAULT_TIMEOUT == 60.0

    def test_default_max_retries(self):
        assert DEFAULT_MAX_RETRIES == 2

    def test_sdk_version_format(self):
        parts = SDK_VERSION.split(".")
        assert len(parts) == 3


class TestHelpers:
    def test_user_agent(self):
        ua = _user_agent()
        assert ua.startswith("bycrawl-python/")
        assert SDK_VERSION in ua

    def test_make_headers(self):
        h = _make_headers("sk_byc_test")
        assert h["x-api-key"] == "sk_byc_test"
        assert "application/json" in h["Accept"]

    def test_backoff_delay_increases(self):
        delays = [_backoff_delay(i, base=1.0, max_delay=100.0) for i in range(5)]
        # Due to jitter, we can't assert strict ordering,
        # but the maximum possible delay should increase
        for i in range(5):
            assert 0 <= delays[i] <= min(1.0 * (2**i), 100.0)


class TestResponseWrapper:
    def test_basic(self):
        w = ResponseWrapper(status_code=200, data={"key": "val"})
        assert w.status_code == 200
        assert w.data == {"key": "val"}
        assert w.headers == {}


class TestRaiseForStatus:
    def test_success_does_nothing(self):
        resp = httpx.Response(200, json={"data": "ok"})
        _raise_for_status(resp)  # should not raise

    def test_401(self):
        resp = httpx.Response(401, json={"error": "bad key"})
        with pytest.raises(AuthenticationError):
            _raise_for_status(resp)

    def test_403(self):
        resp = httpx.Response(403, json={"error": "no scope"})
        with pytest.raises(PermissionError):
            _raise_for_status(resp)

    def test_404(self):
        resp = httpx.Response(404, json={"error": "not found"})
        with pytest.raises(NotFoundError):
            _raise_for_status(resp)

    def test_429(self):
        resp = httpx.Response(
            429,
            json={"error": "rate limit"},
            headers={"retry-after": "5"},
        )
        with pytest.raises(RateLimitError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.retry_after == 5.0

    def test_500(self):
        resp = httpx.Response(500, json={"error": "server error"})
        with pytest.raises(ServerError):
            _raise_for_status(resp)

    def test_502(self):
        resp = httpx.Response(502, json={"error": "bad gateway"})
        with pytest.raises(ServerError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.status_code == 502

    def test_unknown_4xx(self):
        resp = httpx.Response(418, json={"error": "teapot"})
        with pytest.raises(APIError) as exc_info:
            _raise_for_status(resp)
        assert exc_info.value.status_code == 418

    def test_non_json_body(self):
        resp = httpx.Response(500, text="Internal Server Error")
        with pytest.raises(ServerError):
            _raise_for_status(resp)


class TestSyncTransport:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_successful_get(self, respx_mock: respx.Router):
        respx_mock.get("/test").mock(
            return_value=httpx.Response(200, json={"data": "ok"})
        )
        transport = SyncTransport(api_key="sk_byc_test", max_retries=0)
        result = transport.request("GET", "/test")
        assert result.data == {"data": "ok"}
        assert result.status_code == 200
        transport.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_strips_none_params(self, respx_mock: respx.Router):
        route = respx_mock.get("/test").mock(
            return_value=httpx.Response(200, json={"data": "ok"})
        )
        transport = SyncTransport(api_key="sk_byc_test", max_retries=0)
        transport.request("GET", "/test", params={"a": "1", "b": None})
        url = str(route.calls[0].request.url)
        assert "a=1" in url
        assert "b=" not in url
        transport.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_retry_on_500(self, respx_mock: respx.Router):
        respx_mock.get("/test").mock(
            side_effect=[
                httpx.Response(500, json={"error": "fail"}),
                httpx.Response(200, json={"data": "ok"}),
            ]
        )
        transport = SyncTransport(api_key="sk_byc_test", max_retries=1)
        result = transport.request("GET", "/test")
        assert result.data == {"data": "ok"}
        transport.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_raises_after_max_retries(self, respx_mock: respx.Router):
        respx_mock.get("/test").mock(
            return_value=httpx.Response(500, json={"error": "fail"})
        )
        transport = SyncTransport(api_key="sk_byc_test", max_retries=1)
        with pytest.raises(ServerError):
            transport.request("GET", "/test")
        transport.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_invalid_json_response(self, respx_mock: respx.Router):
        respx_mock.get("/test").mock(
            return_value=httpx.Response(200, text="not json", headers={"content-type": "text/plain"})
        )
        transport = SyncTransport(api_key="sk_byc_test", max_retries=0)
        with pytest.raises(APIError, match="Invalid JSON"):
            transport.request("GET", "/test")
        transport.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_no_retry_on_auth_error(self, respx_mock: respx.Router):
        route = respx_mock.get("/test").mock(
            return_value=httpx.Response(401, json={"error": "bad key"})
        )
        transport = SyncTransport(api_key="sk_byc_test", max_retries=2)
        with pytest.raises(AuthenticationError):
            transport.request("GET", "/test")
        assert route.call_count == 1
        transport.close()
