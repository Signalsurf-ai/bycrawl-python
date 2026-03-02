"""
ByCrawl Exception Hierarchy

All SDK exceptions inherit from ByCrawlError.
HTTP errors are mapped to specific subclasses by status code.
"""

from __future__ import annotations


class ByCrawlError(Exception):
    """Base exception for all ByCrawl SDK errors."""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(ByCrawlError):
    """HTTP error returned by the ByCrawl API."""

    status_code: int
    body: dict[str, object] | None

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        body: dict[str, object] | None = None,
    ) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(message)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(status_code={self.status_code}, message={self.message!r})"


class AuthenticationError(APIError):
    """401 - Invalid or missing API key."""

    def __init__(self, message: str = "Invalid or missing API key", **kwargs: object) -> None:
        super().__init__(message, status_code=401, **kwargs)  # type: ignore[arg-type]


class PermissionError(APIError):
    """403 - API key lacks required scope."""

    def __init__(self, message: str = "Insufficient scope", **kwargs: object) -> None:
        super().__init__(message, status_code=403, **kwargs)  # type: ignore[arg-type]


class NotFoundError(APIError):
    """404 - Resource not found."""

    def __init__(self, message: str = "Resource not found", **kwargs: object) -> None:
        super().__init__(message, status_code=404, **kwargs)  # type: ignore[arg-type]


class RateLimitError(APIError):
    """429 - Rate limit or credit limit exceeded."""

    retry_after: float | None

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        *,
        retry_after: float | None = None,
        **kwargs: object,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code=429, **kwargs)  # type: ignore[arg-type]


class ServerError(APIError):
    """5xx - Server-side error."""


class TimeoutError(ByCrawlError):
    """Request timed out."""


class ConnectionError(ByCrawlError):
    """Network connection error."""
