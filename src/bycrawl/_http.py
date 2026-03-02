"""
HTTP Transport Layer

Provides SyncTransport and AsyncTransport that wrap httpx clients with:
- API key authentication (x-api-key header)
- Automatic retry with exponential backoff + jitter
- Consistent error mapping to ByCrawl exceptions
- ResponseWrapper with headers for rate limit / credit parsing
"""

from __future__ import annotations

import json as _json
import random
import time
from dataclasses import dataclass, field
from typing import Any

import httpx
from loguru import logger

from ._exceptions import (
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

DEFAULT_BASE_URL = "https://api.bycrawl.com"
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_RETRIES = 2
SDK_VERSION = "0.1.1"

_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def _user_agent() -> str:
    return f"bycrawl-python/{SDK_VERSION}"


def _make_headers(api_key: str) -> dict[str, str]:
    return {
        "x-api-key": api_key,
        "User-Agent": _user_agent(),
        "Accept": "application/json",
    }


def _backoff_delay(attempt: int, base: float = 0.5, max_delay: float = 8.0) -> float:
    """Exponential backoff with full jitter."""
    delay = min(base * (2**attempt), max_delay)
    return random.uniform(0, delay)  # noqa: S311


@dataclass
class ResponseWrapper:
    """Wraps an HTTP response with parsed JSON body and raw headers."""

    status_code: int
    data: dict[str, Any]
    headers: dict[str, str] = field(default_factory=dict)


def _raise_for_status(response: httpx.Response) -> None:
    """Map HTTP error responses to typed exceptions."""
    if response.is_success:
        return

    status = response.status_code
    try:
        body = response.json()
        message = body.get("error", response.reason_phrase or "Unknown error")
    except Exception:
        body = None
        message = response.reason_phrase or f"HTTP {status}"

    if status == 401:
        raise AuthenticationError(message, body=body)
    if status == 403:
        raise PermissionError(message, body=body)
    if status == 404:
        raise NotFoundError(message, body=body)
    if status == 429:
        retry_after = response.headers.get("retry-after")
        raise RateLimitError(
            message,
            retry_after=float(retry_after) if retry_after else None,
            body=body,
        )
    if 500 <= status < 600:
        raise ServerError(message, status_code=status, body=body)

    raise APIError(message, status_code=status, body=body)


class SyncTransport:
    """Synchronous HTTP transport with retry logic."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = http_client or httpx.Client(
            base_url=self._base_url,
            headers=_make_headers(api_key),
            timeout=timeout,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> ResponseWrapper:
        """Make an HTTP request with retry logic. Returns ResponseWrapper."""
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        last_exc: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                logger.debug("Request {} {} attempt={}", method, path, attempt)
                response = self._client.request(
                    method,
                    path,
                    params=params,
                    json=json,
                    headers=headers,
                )

                if response.status_code in _RETRYABLE_STATUS_CODES and attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    if response.status_code == 429:
                        retry_after = response.headers.get("retry-after")
                        if retry_after:
                            delay = max(delay, float(retry_after))
                    logger.warning(
                        "Retrying {} {} status={} delay={:.2f}s",
                        method, path, response.status_code, delay,
                    )
                    time.sleep(delay)
                    continue

                _raise_for_status(response)

                try:
                    data = response.json()
                except _json.JSONDecodeError as exc:
                    raise APIError(
                        "Invalid JSON response", status_code=502
                    ) from exc

                return ResponseWrapper(
                    status_code=response.status_code,
                    data=data,
                    headers=dict(response.headers),
                )

            except (AuthenticationError, PermissionError, NotFoundError, RateLimitError,
                    ServerError, APIError):
                raise
            except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.warning("Connection error, retrying in {:.2f}s: {}", delay, exc)
                    time.sleep(delay)
                    continue
                logger.error("Connection failed after {} retries: {}", self._max_retries, exc)
                raise ConnectionError(str(exc)) from exc
            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.warning("Timeout, retrying in {:.2f}s: {}", delay, exc)
                    time.sleep(delay)
                    continue
                logger.error("Timeout after {} retries: {}", self._max_retries, exc)
                raise TimeoutError(str(exc)) from exc
            except ByCrawlError:
                raise
            except Exception as exc:
                raise ByCrawlError(f"Unexpected error: {exc}") from exc

        if last_exc:
            raise ConnectionError(str(last_exc)) from last_exc
        raise ConnectionError("Request failed after retries")

    def close(self) -> None:
        self._client.close()


class AsyncTransport:
    """Asynchronous HTTP transport with retry logic."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = http_client or httpx.AsyncClient(
            base_url=self._base_url,
            headers=_make_headers(api_key),
            timeout=timeout,
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> ResponseWrapper:
        """Make an async HTTP request with retry logic. Returns ResponseWrapper."""
        import asyncio

        if params:
            params = {k: v for k, v in params.items() if v is not None}

        last_exc: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                logger.debug("Async request {} {} attempt={}", method, path, attempt)
                response = await self._client.request(
                    method,
                    path,
                    params=params,
                    json=json,
                    headers=headers,
                )

                if response.status_code in _RETRYABLE_STATUS_CODES and attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    if response.status_code == 429:
                        retry_after = response.headers.get("retry-after")
                        if retry_after:
                            delay = max(delay, float(retry_after))
                    logger.warning(
                        "Retrying async {} {} status={} delay={:.2f}s",
                        method, path, response.status_code, delay,
                    )
                    await asyncio.sleep(delay)
                    continue

                _raise_for_status(response)

                try:
                    data = response.json()
                except _json.JSONDecodeError as exc:
                    raise APIError(
                        "Invalid JSON response", status_code=502
                    ) from exc

                return ResponseWrapper(
                    status_code=response.status_code,
                    data=data,
                    headers=dict(response.headers),
                )

            except (AuthenticationError, PermissionError, NotFoundError, RateLimitError,
                    ServerError, APIError):
                raise
            except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.warning("Connection error, retrying in {:.2f}s: {}", delay, exc)
                    await asyncio.sleep(delay)
                    continue
                logger.error("Connection failed after {} retries: {}", self._max_retries, exc)
                raise ConnectionError(str(exc)) from exc
            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.warning("Timeout, retrying in {:.2f}s: {}", delay, exc)
                    await asyncio.sleep(delay)
                    continue
                logger.error("Timeout after {} retries: {}", self._max_retries, exc)
                raise TimeoutError(str(exc)) from exc
            except ByCrawlError:
                raise
            except Exception as exc:
                raise ByCrawlError(f"Unexpected error: {exc}") from exc

        if last_exc:
            raise ConnectionError(str(last_exc)) from last_exc
        raise ConnectionError("Request failed after retries")

    async def close(self) -> None:
        await self._client.aclose()
