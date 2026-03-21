"""591 Rent platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse


class Rent591(APIResource):
    """Sync 591 Rent namespace."""

    def get_listings(
        self,
        *,
        region: int | None = None,
        first_row: int | None = None,
        kind: int | None = None,
        section: int | None = None,
        price: str | None = None,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/rent591/listings",
            params={
                "region": region,
                "first_row": first_row,
                "kind": kind,
                "section": section,
                "price": price,
                "count": count,
            },
        )

    def get_listing(self, listing_id: int) -> APIResponse[dict[str, Any]]:
        return self._get(f"/rent591/listings/{listing_id}")


class AsyncRent591(AsyncAPIResource):
    """Async 591 Rent namespace."""

    async def get_listings(
        self,
        *,
        region: int | None = None,
        first_row: int | None = None,
        kind: int | None = None,
        section: int | None = None,
        price: str | None = None,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/rent591/listings",
            params={
                "region": region,
                "first_row": first_row,
                "kind": kind,
                "section": section,
                "price": price,
                "count": count,
            },
        )

    async def get_listing(self, listing_id: int) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/rent591/listings/{listing_id}")
