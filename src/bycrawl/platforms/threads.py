"""Threads platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import (
    APIResponse,
    ThreadsPost,
    ThreadsUser,
)


class Threads(APIResource):
    """Sync Threads namespace."""

    def get_post(self, post_id: str) -> APIResponse[ThreadsPost]:
        return self._get(f"/threads/posts/{post_id}", cast_to=ThreadsPost)

    def get_posts(
        self, ids: list[str]
    ) -> APIResponse[list[ThreadsPost]]:
        return self._get(
            "/threads/posts",
            params={"ids": ",".join(ids)},
            cast_to=ThreadsPost,
        )

    def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        search_type: str | None = None,
        cursor: str | None = None,
    ) -> APIResponse[list[ThreadsPost]]:
        return self._get_list(
            "/threads/posts/search",
            params={
                "q": q,
                "count": count,
                "search_type": search_type,
                "cursor": cursor,
            },
            items_key="posts",
            cast_to=ThreadsPost,
        )

    def get_post_replies(self, post_id: str) -> APIResponse[dict[str, Any]]:
        """Get direct replies to a Threads post.

        Returns ``{rootPost, replies, totalReplies, hasMore}``. Anonymous SSR
        embeds ~20 top-level replies per post; pagination is not supported.
        """
        return self._get(f"/threads/posts/{post_id}/replies")

    def get_user(self, username: str) -> APIResponse[ThreadsUser]:
        return self._get(f"/threads/users/{username}", cast_to=ThreadsUser)

    def get_user_posts(
        self,
        user_id: str,
        *,
        cursor: str | None = None,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/threads/users/{user_id}/posts",
            params={"cursor": cursor, "count": count},
        )

    def get_user_replies(
        self,
        user_id: str,
        *,
        cursor: str | None = None,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/threads/users/{user_id}/replies",
            params={"cursor": cursor, "count": count},
        )

    def search_users(
        self, q: str, *, count: int | None = None
    ) -> APIResponse[list[ThreadsUser]]:
        return self._get_list(
            "/threads/users/search",
            params={"q": q, "count": count},
            items_key="users",
            cast_to=ThreadsUser,
        )

    def get_public_feed(
        self,
        *,
        cursor: str | None = None,
        count: int | None = None,
        country: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/threads/feed/public",
            params={"cursor": cursor, "count": count, "country": country},
        )

    # -- Auto-pagination iterators --

    def iter_user_posts(
        self, user_id: str, *, count: int | None = None
    ) -> Iterator[ThreadsPost]:
        return self._paginate(
            f"/threads/users/{user_id}/posts",
            params={"count": count},
            items_key="posts",
            cast_to=ThreadsPost,
        )

    def iter_user_replies(
        self, user_id: str, *, count: int | None = None
    ) -> Iterator[ThreadsPost]:
        return self._paginate(
            f"/threads/users/{user_id}/replies",
            params={"count": count},
            items_key="replies",
            cast_to=ThreadsPost,
        )


class AsyncThreads(AsyncAPIResource):
    """Async Threads namespace."""

    async def get_post(
        self, post_id: str
    ) -> APIResponse[ThreadsPost]:
        return await self._get(
            f"/threads/posts/{post_id}", cast_to=ThreadsPost
        )

    async def get_posts(
        self, ids: list[str]
    ) -> APIResponse[list[ThreadsPost]]:
        return await self._get(
            "/threads/posts",
            params={"ids": ",".join(ids)},
            cast_to=ThreadsPost,
        )

    async def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        search_type: str | None = None,
        cursor: str | None = None,
    ) -> APIResponse[list[ThreadsPost]]:
        return await self._get_list(
            "/threads/posts/search",
            params={
                "q": q,
                "count": count,
                "search_type": search_type,
                "cursor": cursor,
            },
            items_key="posts",
            cast_to=ThreadsPost,
        )

    async def get_post_replies(self, post_id: str) -> APIResponse[dict[str, Any]]:
        """Get direct replies to a Threads post.

        Returns ``{rootPost, replies, totalReplies, hasMore}``. Anonymous SSR
        embeds ~20 top-level replies per post; pagination is not supported.
        """
        return await self._get(f"/threads/posts/{post_id}/replies")

    async def get_user(self, username: str) -> APIResponse[ThreadsUser]:
        return await self._get(f"/threads/users/{username}", cast_to=ThreadsUser)

    async def get_user_posts(
        self,
        user_id: str,
        *,
        cursor: str | None = None,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/threads/users/{user_id}/posts",
            params={"cursor": cursor, "count": count},
        )

    async def get_user_replies(
        self,
        user_id: str,
        *,
        cursor: str | None = None,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/threads/users/{user_id}/replies",
            params={"cursor": cursor, "count": count},
        )

    async def search_users(
        self, q: str, *, count: int | None = None
    ) -> APIResponse[list[ThreadsUser]]:
        return await self._get_list(
            "/threads/users/search",
            params={"q": q, "count": count},
            items_key="users",
            cast_to=ThreadsUser,
        )

    async def get_public_feed(
        self,
        *,
        cursor: str | None = None,
        count: int | None = None,
        country: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/threads/feed/public",
            params={"cursor": cursor, "count": count, "country": country},
        )

    # -- Auto-pagination iterators --

    async def iter_user_posts(
        self, user_id: str, *, count: int | None = None
    ) -> AsyncIterator[ThreadsPost]:
        async for item in self._paginate(
            f"/threads/users/{user_id}/posts",
            params={"count": count},
            items_key="posts",
            cast_to=ThreadsPost,
        ):
            yield item

    async def iter_user_replies(
        self, user_id: str, *, count: int | None = None
    ) -> AsyncIterator[ThreadsPost]:
        async for item in self._paginate(
            f"/threads/users/{user_id}/replies",
            params={"count": count},
            items_key="replies",
            cast_to=ThreadsPost,
        ):
            yield item
