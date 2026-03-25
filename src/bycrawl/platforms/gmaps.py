"""Google Maps platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, GMapsPlace


class GMaps(APIResource):
    """Sync Google Maps namespace."""

    def search(
        self,
        q: str,
        *,
        language: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/gmaps/places/search", params={"q": q, "language": language}
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

    def get_place_reviews(
        self,
        query: str,
        *,
        sort: str | None = None,
        page_token: str | None = None,
        language: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/gmaps/places/reviews",
            params={
                "query": query,
                "sort": sort,
                "pageToken": page_token,
                "language": language,
            },
        )


class AsyncGMaps(AsyncAPIResource):
    """Async Google Maps namespace."""

    async def search(
        self,
        q: str,
        *,
        language: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/gmaps/places/search", params={"q": q, "language": language}
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

    async def get_place_reviews(
        self,
        query: str,
        *,
        sort: str | None = None,
        page_token: str | None = None,
        language: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/gmaps/places/reviews",
            params={
                "query": query,
                "sort": sort,
                "pageToken": page_token,
                "language": language,
            },
        )
