"""Google Maps platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, GMapsPlace


class GMaps(APIResource):
    """Sync Google Maps namespace."""

    def search(
        self,
        query: str,
        *,
        language: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/gmaps/search", params={"query": query, "language": language}
        )

    def get_place(
        self,
        query: str,
        *,
        language: str | None = None,
    ) -> APIResponse[GMapsPlace]:
        return self._get(
            "/gmaps/places",
            params={"query": query, "language": language},
            cast_to=GMapsPlace,
        )


class AsyncGMaps(AsyncAPIResource):
    """Async Google Maps namespace."""

    async def search(
        self,
        query: str,
        *,
        language: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/gmaps/search", params={"query": query, "language": language}
        )

    async def get_place(
        self,
        query: str,
        *,
        language: str | None = None,
    ) -> APIResponse[GMapsPlace]:
        return await self._get(
            "/gmaps/places",
            params={"query": query, "language": language},
            cast_to=GMapsPlace,
        )
