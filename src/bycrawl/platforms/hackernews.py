"""Hacker News platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse


class HackerNews(APIResource):
    """Sync Hacker News namespace."""

    def get_item(self, item_id: int) -> APIResponse[dict[str, Any]]:
        return self._get(f"/hackernews/items/{item_id}")

    def get_user(self, username: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/hackernews/users/{username}")

    def get_stories(
        self,
        story_type: str,
        *,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/hackernews/stories/{story_type}",
            params={"count": count},
        )

    def get_item_comments(
        self,
        item_id: int,
        *,
        depth: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/hackernews/items/{item_id}/comments",
            params={"depth": depth},
        )


class AsyncHackerNews(AsyncAPIResource):
    """Async Hacker News namespace."""

    async def get_item(self, item_id: int) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/hackernews/items/{item_id}")

    async def get_user(self, username: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/hackernews/users/{username}")

    async def get_stories(
        self,
        story_type: str,
        *,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/hackernews/stories/{story_type}",
            params={"count": count},
        )

    async def get_item_comments(
        self,
        item_id: int,
        *,
        depth: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/hackernews/items/{item_id}/comments",
            params={"depth": depth},
        )
