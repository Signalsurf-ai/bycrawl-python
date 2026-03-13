"""Tests for exception hierarchy."""

from __future__ import annotations

from bycrawl import (
    APIError,
    AuthenticationError,
    ByCrawlError,
    ConnectionError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ServerError,
    TimeoutError,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_bycrawl_error(self):
        for exc_cls in [
            APIError, AuthenticationError, PermissionError,
            NotFoundError, RateLimitError, ServerError,
        ]:
            assert issubclass(exc_cls, ByCrawlError)

    def test_timeout_and_connection_inherit_from_base(self):
        assert issubclass(TimeoutError, ByCrawlError)
        assert issubclass(ConnectionError, ByCrawlError)

    def test_api_error_attributes(self):
        err = APIError("bad request", status_code=400, body={"detail": "oops"})
        assert err.status_code == 400
        assert err.body == {"detail": "oops"}
        assert err.message == "bad request"

    def test_authentication_error_defaults(self):
        err = AuthenticationError()
        assert err.status_code == 401
        assert "Invalid or missing API key" in err.message

    def test_permission_error_defaults(self):
        err = PermissionError()
        assert err.status_code == 403

    def test_not_found_error_defaults(self):
        err = NotFoundError()
        assert err.status_code == 404

    def test_rate_limit_error_retry_after(self):
        err = RateLimitError(retry_after=5.0)
        assert err.status_code == 429
        assert err.retry_after == 5.0

    def test_server_error(self):
        err = ServerError("down", status_code=502)
        assert err.status_code == 502

    def test_api_error_repr(self):
        err = APIError("test", status_code=418)
        assert "418" in repr(err)
        assert "test" in repr(err)
