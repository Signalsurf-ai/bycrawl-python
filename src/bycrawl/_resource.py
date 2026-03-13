"""
APIResource Base Classes

All platform namespaces inherit from APIResource (sync) or AsyncAPIResource (async).
Handles HTTP call delegation, response wrapping, header parsing, and pagination.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from ._exceptions import ByCrawlError
from ._http import AsyncTransport, ResponseWrapper, SyncTransport
from ._types import APIResponse, CreditInfo, RateLimit

T = TypeVar("T")
_ModelT = type[BaseModel]


def _parse_rate_limit(headers: dict[str, str]) -> RateLimit | None:
    """Parse rate limit info from response headers."""
    limit = headers.get("x-ratelimit-limit")
    remaining = headers.get("x-ratelimit-remaining")
    reset = headers.get("x-ratelimit-reset")
    if limit is None and remaining is None and reset is None:
        return None
    return RateLimit(
        limit=int(limit) if limit else None,
        remaining=int(remaining) if remaining else None,
        reset=float(reset) if reset else None,
    )


def _parse_credit(headers: dict[str, str]) -> CreditInfo | None:
    """Parse credit info from response headers."""
    remaining = headers.get("x-credit-remaining")
    used = headers.get("x-credit-used")
    if remaining is None and used is None:
        return None
    return CreditInfo(
        remaining=int(remaining) if remaining else None,
        used=int(used) if used else None,
    )


def _wrap_response(wrapper: ResponseWrapper, cast_to: _ModelT | None = None) -> APIResponse:  # type: ignore[type-arg]
    """Build an APIResponse from a ResponseWrapper."""
    data = wrapper.data
    if isinstance(data, dict) and "data" in data:
        body_data = data["data"]
        success = data.get("success", True)
        error = data.get("error")
        queued = data.get("queued", False)
    elif isinstance(data, dict) and "error" in data:
        body_data = None
        success = False
        error = data.get("error")
        queued = False
    else:
        # API returns raw data without envelope
        body_data = data
        success = True
        error = None
        queued = False

    parsed: Any = body_data
    if cast_to is not None and body_data is not None:
        try:
            if isinstance(body_data, list):
                parsed = [cast_to.model_validate(item) for item in body_data]
            elif isinstance(body_data, dict):
                parsed = cast_to.model_validate(body_data)
        except ValidationError as exc:
            raise ByCrawlError(f"Response parsing failed: {exc}") from exc

    return APIResponse(
        success=success,
        data=parsed,
        error=error,
        queued=queued,
        rate_limit=_parse_rate_limit(wrapper.headers),
        credit=_parse_credit(wrapper.headers),
    )


class APIResource:
    """Sync base class for all platform namespaces."""

    def __init__(self, transport: SyncTransport) -> None:
        self._transport = transport

    def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        cast_to: _ModelT | None = None,
    ) -> APIResponse:  # type: ignore[type-arg]
        return self._request("GET", path, params=params, cast_to=cast_to)

    def _post(
        self,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        cast_to: _ModelT | None = None,
    ) -> APIResponse:  # type: ignore[type-arg]
        return self._request("POST", path, body=body, cast_to=cast_to)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        cast_to: _ModelT | None = None,
    ) -> APIResponse:  # type: ignore[type-arg]
        wrapper = self._transport.request(method, path, params=params, json=body)
        return _wrap_response(wrapper, cast_to=cast_to)

    def _paginate(
        self,
        path: str,
        *,
        params: dict[str, Any],
        items_key: str = "items",
        cursor_key: str = "cursor",
        has_more_key: str = "hasMore",
        cast_to: _ModelT | None = None,
    ) -> Iterator[Any]:
        """Cursor-based auto-pagination."""
        while True:
            wrapper = self._transport.request("GET", path, params=params)
            data = wrapper.data.get("data", wrapper.data)
            items = data.get(items_key, [])
            for item in items:
                if cast_to is not None:
                    try:
                        yield cast_to.model_validate(item)
                    except ValidationError as exc:
                        raise ByCrawlError(f"Response parsing failed: {exc}") from exc
                else:
                    yield item
            if not data.get(has_more_key, False):
                break
            next_cursor = data.get(cursor_key) or data.get("next_cursor")
            if not next_cursor:
                break
            params = {**params, cursor_key: next_cursor}

    def _paginate_by_page(
        self,
        path: str,
        *,
        params: dict[str, Any],
        items_key: str = "items",
        page_key: str = "page",
        cast_to: _ModelT | None = None,
    ) -> Iterator[Any]:
        """Page-number based auto-pagination."""
        page = params.get(page_key, 1)
        while True:
            params = {**params, page_key: page}
            wrapper = self._transport.request("GET", path, params=params)
            data = wrapper.data.get("data", wrapper.data)
            items = data.get(items_key, [])
            if not items:
                break
            for item in items:
                if cast_to is not None:
                    try:
                        yield cast_to.model_validate(item)
                    except ValidationError as exc:
                        raise ByCrawlError(f"Response parsing failed: {exc}") from exc
                else:
                    yield item
            if not data.get("hasMore", len(items) >= params.get("limit", 20)):
                break
            page += 1

    def _paginate_by_offset(
        self,
        path: str,
        *,
        params: dict[str, Any],
        items_key: str = "items",
        count_key: str = "count",
        cast_to: _ModelT | None = None,
    ) -> Iterator[Any]:
        """Offset-based auto-pagination."""
        offset = params.get("offset", 0)
        limit = params.get("limit", 20)
        while True:
            params = {**params, "offset": offset, "limit": limit}
            wrapper = self._transport.request("GET", path, params=params)
            data = wrapper.data.get("data", wrapper.data)
            items = data.get(items_key, [])
            if not items:
                break
            for item in items:
                if cast_to is not None:
                    try:
                        yield cast_to.model_validate(item)
                    except ValidationError as exc:
                        raise ByCrawlError(f"Response parsing failed: {exc}") from exc
                else:
                    yield item
            total = data.get(count_key)
            offset += len(items)
            if total is not None and offset >= total:
                break
            if len(items) < limit:
                break


class AsyncAPIResource:
    """Async base class for all platform namespaces."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._transport = transport

    async def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        cast_to: _ModelT | None = None,
    ) -> APIResponse:  # type: ignore[type-arg]
        return await self._request("GET", path, params=params, cast_to=cast_to)

    async def _post(
        self,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        cast_to: _ModelT | None = None,
    ) -> APIResponse:  # type: ignore[type-arg]
        return await self._request("POST", path, body=body, cast_to=cast_to)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        cast_to: _ModelT | None = None,
    ) -> APIResponse:  # type: ignore[type-arg]
        wrapper = await self._transport.request(method, path, params=params, json=body)
        return _wrap_response(wrapper, cast_to=cast_to)

    async def _paginate(
        self,
        path: str,
        *,
        params: dict[str, Any],
        items_key: str = "items",
        cursor_key: str = "cursor",
        has_more_key: str = "hasMore",
        cast_to: _ModelT | None = None,
    ) -> AsyncIterator[Any]:
        """Cursor-based async auto-pagination."""
        while True:
            wrapper = await self._transport.request("GET", path, params=params)
            data = wrapper.data.get("data", wrapper.data)
            items = data.get(items_key, [])
            for item in items:
                if cast_to is not None:
                    try:
                        yield cast_to.model_validate(item)
                    except ValidationError as exc:
                        raise ByCrawlError(f"Response parsing failed: {exc}") from exc
                else:
                    yield item
            if not data.get(has_more_key, False):
                break
            next_cursor = data.get(cursor_key) or data.get("next_cursor")
            if not next_cursor:
                break
            params = {**params, cursor_key: next_cursor}

    async def _paginate_by_page(
        self,
        path: str,
        *,
        params: dict[str, Any],
        items_key: str = "items",
        page_key: str = "page",
        cast_to: _ModelT | None = None,
    ) -> AsyncIterator[Any]:
        """Page-number based async auto-pagination."""
        page = params.get(page_key, 1)
        while True:
            params = {**params, page_key: page}
            wrapper = await self._transport.request("GET", path, params=params)
            data = wrapper.data.get("data", wrapper.data)
            items = data.get(items_key, [])
            if not items:
                break
            for item in items:
                if cast_to is not None:
                    try:
                        yield cast_to.model_validate(item)
                    except ValidationError as exc:
                        raise ByCrawlError(f"Response parsing failed: {exc}") from exc
                else:
                    yield item
            if not data.get("hasMore", len(items) >= params.get("limit", 20)):
                break
            page += 1

    async def _paginate_by_offset(
        self,
        path: str,
        *,
        params: dict[str, Any],
        items_key: str = "items",
        count_key: str = "count",
        cast_to: _ModelT | None = None,
    ) -> AsyncIterator[Any]:
        """Offset-based async auto-pagination."""
        offset = params.get("offset", 0)
        limit = params.get("limit", 20)
        while True:
            params = {**params, "offset": offset, "limit": limit}
            wrapper = await self._transport.request("GET", path, params=params)
            data = wrapper.data.get("data", wrapper.data)
            items = data.get(items_key, [])
            if not items:
                break
            for item in items:
                if cast_to is not None:
                    try:
                        yield cast_to.model_validate(item)
                    except ValidationError as exc:
                        raise ByCrawlError(f"Response parsing failed: {exc}") from exc
                else:
                    yield item
            total = data.get(count_key)
            offset += len(items)
            if total is not None and offset >= total:
                break
            if len(items) < limit:
                break
