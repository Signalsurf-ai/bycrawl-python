"""Trustpilot platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse


class Trustpilot(APIResource):
    """Sync Trustpilot namespace."""

    def get_business(self, domain: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/trustpilot/businesses/{domain}")

    def get_business_reviews(
        self,
        domain: str,
        *,
        page: int | None = None,
        sort: str | None = None,
        stars: int | None = None,
        languages: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/trustpilot/businesses/{domain}/reviews",
            params={
                "page": page,
                "sort": sort,
                "stars": stars,
                "languages": languages,
            },
        )

    def search_businesses(
        self,
        q: str,
        *,
        page: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/trustpilot/businesses/search",
            params={"q": q, "page": page},
        )

    def search_categories(self, q: str) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/trustpilot/categories/search",
            params={"q": q},
        )

    def get_suggestions(self, q: str) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/trustpilot/suggestions",
            params={"q": q},
        )


class AsyncTrustpilot(AsyncAPIResource):
    """Async Trustpilot namespace."""

    async def get_business(self, domain: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/trustpilot/businesses/{domain}")

    async def get_business_reviews(
        self,
        domain: str,
        *,
        page: int | None = None,
        sort: str | None = None,
        stars: int | None = None,
        languages: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/trustpilot/businesses/{domain}/reviews",
            params={
                "page": page,
                "sort": sort,
                "stars": stars,
                "languages": languages,
            },
        )

    async def search_businesses(
        self,
        q: str,
        *,
        page: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/trustpilot/businesses/search",
            params={"q": q, "page": page},
        )

    async def search_categories(self, q: str) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/trustpilot/categories/search",
            params={"q": q},
        )

    async def get_suggestions(self, q: str) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/trustpilot/suggestions",
            params={"q": q},
        )
