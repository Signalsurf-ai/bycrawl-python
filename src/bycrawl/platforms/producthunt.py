"""Product Hunt platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse


class ProductHunt(APIResource):
    """Sync Product Hunt namespace."""

    def get_posts(
        self,
        *,
        count: int | None = None,
        date: str | None = None,
        period: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/producthunt/posts",
            params={"count": count, "date": date, "period": period},
        )

    def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/producthunt/posts/search",
            params={"q": q, "count": count},
        )

    def get_post(self, slug: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/producthunt/posts/{slug}")

    def get_reviews(self, slug: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/producthunt/posts/{slug}/reviews")


class AsyncProductHunt(AsyncAPIResource):
    """Async Product Hunt namespace."""

    async def get_posts(
        self,
        *,
        count: int | None = None,
        date: str | None = None,
        period: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/producthunt/posts",
            params={"count": count, "date": date, "period": period},
        )

    async def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/producthunt/posts/search",
            params={"q": q, "count": count},
        )

    async def get_post(self, slug: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/producthunt/posts/{slug}")

    async def get_reviews(self, slug: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/producthunt/posts/{slug}/reviews")
