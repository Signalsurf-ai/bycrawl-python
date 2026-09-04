"""Google SERP platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse


class Google(APIResource):
    """Sync Google namespace."""

    def search(
        self,
        q: str,
        *,
        num: int | None = None,
        language: str | None = None,
        country: str | None = None,
        page: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/google/search",
            params={
                "q": q,
                "num": num,
                "language": language,
                "country": country,
                "page": page,
            },
        )

    def news(
        self,
        q: str,
        *,
        language: str | None = None,
        country: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/google/news",
            params={"q": q, "language": language, "country": country},
        )

    def shopping(
        self,
        q: str,
        *,
        num: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        country: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/google/shopping",
            params={
                "q": q,
                "num": num,
                "min_price": min_price,
                "max_price": max_price,
                "country": country,
            },
        )


class AsyncGoogle(AsyncAPIResource):
    """Async Google namespace."""

    async def search(
        self,
        q: str,
        *,
        num: int | None = None,
        language: str | None = None,
        country: str | None = None,
        page: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/google/search",
            params={
                "q": q,
                "num": num,
                "language": language,
                "country": country,
                "page": page,
            },
        )

    async def news(
        self,
        q: str,
        *,
        language: str | None = None,
        country: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/google/news",
            params={"q": q, "language": language, "country": country},
        )

    async def shopping(
        self,
        q: str,
        *,
        num: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        country: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/google/shopping",
            params={
                "q": q,
                "num": num,
                "min_price": min_price,
                "max_price": max_price,
                "country": country,
            },
        )
