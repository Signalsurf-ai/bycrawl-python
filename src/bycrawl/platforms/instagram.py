"""Instagram platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, InstagramUser


class Instagram(APIResource):
    """Sync Instagram namespace."""

    def get_user(self, username: str) -> APIResponse[InstagramUser]:
        return self._get(f"/instagram/users/{username}", cast_to=InstagramUser)

    def search_tags(self, q: str) -> APIResponse[dict[str, Any]]:
        return self._get("/instagram/tags/search", params={"q": q})

    def get_post(self, shortcode: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/instagram/posts/{shortcode}")

    def get_post_comments(
        self, shortcode: str, *, cursor: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/instagram/posts/{shortcode}/comments", params={"cursor": cursor}
        )

    def get_user_posts(
        self, username: str, *, cursor: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/instagram/users/{username}/posts", params={"cursor": cursor}
        )

    # -- Auto-pagination iterators --

    def iter_user_posts(self, username: str) -> Iterator[dict[str, Any]]:
        return self._paginate(
            f"/instagram/users/{username}/posts",
            params={},
            items_key="posts",
        )

    def iter_post_comments(self, shortcode: str) -> Iterator[dict[str, Any]]:
        return self._paginate(
            f"/instagram/posts/{shortcode}/comments",
            params={},
            items_key="comments",
        )


class AsyncInstagram(AsyncAPIResource):
    """Async Instagram namespace."""

    async def get_user(self, username: str) -> APIResponse[InstagramUser]:
        return await self._get(f"/instagram/users/{username}", cast_to=InstagramUser)

    async def search_tags(self, q: str) -> APIResponse[dict[str, Any]]:
        return await self._get("/instagram/tags/search", params={"q": q})

    async def get_post(self, shortcode: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/instagram/posts/{shortcode}")

    async def get_post_comments(
        self, shortcode: str, *, cursor: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/instagram/posts/{shortcode}/comments", params={"cursor": cursor}
        )

    async def get_user_posts(
        self, username: str, *, cursor: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/instagram/users/{username}/posts", params={"cursor": cursor}
        )

    # -- Auto-pagination iterators --

    async def iter_user_posts(self, username: str) -> AsyncIterator[dict[str, Any]]:
        async for item in self._paginate(
            f"/instagram/users/{username}/posts",
            params={},
            items_key="posts",
        ):
            yield item

    async def iter_post_comments(
        self, shortcode: str
    ) -> AsyncIterator[dict[str, Any]]:
        async for item in self._paginate(
            f"/instagram/posts/{shortcode}/comments",
            params={},
            items_key="comments",
        ):
            yield item
