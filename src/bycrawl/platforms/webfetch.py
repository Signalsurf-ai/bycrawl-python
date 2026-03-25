"""Web Fetch platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse


class WebFetch(APIResource):
    """Sync Web Fetch namespace."""

    def fetch(
        self,
        url: str,
        *,
        format: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get("/web/fetch", params={"url": url, "format": format})

    def search(
        self,
        q: str,
        *,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get("/web/search", params={"q": q, "count": count})


class AsyncWebFetch(AsyncAPIResource):
    """Async Web Fetch namespace."""

    async def fetch(
        self,
        url: str,
        *,
        format: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get("/web/fetch", params={"url": url, "format": format})

    async def search(
        self,
        q: str,
        *,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get("/web/search", params={"q": q, "count": count})
