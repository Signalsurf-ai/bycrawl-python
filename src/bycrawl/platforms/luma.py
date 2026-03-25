"""Luma platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse


class Luma(APIResource):
    """Sync Luma namespace."""

    def get_event(self, event_id: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/luma/events/{event_id}")

    def get_place_events(
        self,
        place_id: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/luma/places/{place_id}/events",
            params={"count": count, "cursor": cursor},
        )

    def search_events(
        self,
        place_id: str,
        q: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/luma/events/search",
            params={
                "place_id": place_id,
                "q": q,
                "count": count,
                "cursor": cursor,
            },
        )

    def get_categories(self) -> APIResponse[dict[str, Any]]:
        return self._get("/luma/categories")

    def get_calendar_events(
        self,
        calendar_id: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/luma/calendars/{calendar_id}/events",
            params={"count": count, "cursor": cursor},
        )

    def get_place(self, place_id: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/luma/places/{place_id}")


class AsyncLuma(AsyncAPIResource):
    """Async Luma namespace."""

    async def get_event(self, event_id: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/luma/events/{event_id}")

    async def get_place_events(
        self,
        place_id: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/luma/places/{place_id}/events",
            params={"count": count, "cursor": cursor},
        )

    async def search_events(
        self,
        place_id: str,
        q: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/luma/events/search",
            params={
                "place_id": place_id,
                "q": q,
                "count": count,
                "cursor": cursor,
            },
        )

    async def get_categories(self) -> APIResponse[dict[str, Any]]:
        return await self._get("/luma/categories")

    async def get_calendar_events(
        self,
        calendar_id: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/luma/calendars/{calendar_id}/events",
            params={"count": count, "cursor": cursor},
        )

    async def get_place(self, place_id: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/luma/places/{place_id}")
