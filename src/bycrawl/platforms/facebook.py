"""Facebook platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, FacebookPost, FacebookUser


class Facebook(APIResource):
    """Sync Facebook namespace."""

    def get_user(self, username: str) -> APIResponse[FacebookUser]:
        return self._get(f"/facebook/users/{username}", cast_to=FacebookUser)

    def get_user_posts(self, username: str) -> APIResponse[list[FacebookPost]]:
        return self._get(f"/facebook/users/{username}/posts", cast_to=FacebookPost)

    def get_post(self, *, url: str) -> APIResponse[FacebookPost]:
        return self._get("/facebook/posts", params={"url": url}, cast_to=FacebookPost)

    def get_post_comments(
        self, *, url: str, cursor: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/facebook/posts/comments", params={"url": url, "cursor": cursor}
        )

    def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/facebook/posts/search",
            params={"q": q, "count": count, "cursor": cursor},
        )

    def marketplace_browse(
        self,
        location: str,
        *,
        category: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/facebook/marketplace/listings",
            params={"location": location, "category": category},
        )

    def marketplace_search(
        self,
        q: str,
        *,
        location: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/facebook/marketplace/search",
            params={"q": q, "location": location},
        )

    def marketplace_item(self, listing_id: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/facebook/marketplace/items/{listing_id}")

    # -- Auto-pagination iterators --

    def iter_post_comments(self, *, url: str) -> Iterator[dict[str, Any]]:
        return self._paginate(
            "/facebook/posts/comments",
            params={"url": url},
            items_key="comments",
        )

    def iter_search_posts(
        self, q: str, *, count: int | None = None
    ) -> Iterator[FacebookPost]:
        return self._paginate(
            "/facebook/posts/search",
            params={"q": q, "count": count},
            items_key="posts",
            cast_to=FacebookPost,
        )


class AsyncFacebook(AsyncAPIResource):
    """Async Facebook namespace."""

    async def get_user(self, username: str) -> APIResponse[FacebookUser]:
        return await self._get(f"/facebook/users/{username}", cast_to=FacebookUser)

    async def get_user_posts(self, username: str) -> APIResponse[list[FacebookPost]]:
        return await self._get(f"/facebook/users/{username}/posts", cast_to=FacebookPost)

    async def get_post(self, *, url: str) -> APIResponse[FacebookPost]:
        return await self._get("/facebook/posts", params={"url": url}, cast_to=FacebookPost)

    async def get_post_comments(
        self, *, url: str, cursor: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/facebook/posts/comments", params={"url": url, "cursor": cursor}
        )

    async def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/facebook/posts/search",
            params={"q": q, "count": count, "cursor": cursor},
        )

    async def marketplace_browse(
        self,
        location: str,
        *,
        category: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/facebook/marketplace/listings",
            params={"location": location, "category": category},
        )

    async def marketplace_search(
        self,
        q: str,
        *,
        location: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/facebook/marketplace/search",
            params={"q": q, "location": location},
        )

    async def marketplace_item(self, listing_id: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/facebook/marketplace/items/{listing_id}")

    # -- Auto-pagination iterators --

    async def iter_post_comments(self, *, url: str) -> AsyncIterator[dict[str, Any]]:
        async for item in self._paginate(
            "/facebook/posts/comments",
            params={"url": url},
            items_key="comments",
        ):
            yield item

    async def iter_search_posts(
        self, q: str, *, count: int | None = None
    ) -> AsyncIterator[FacebookPost]:
        async for item in self._paginate(
            "/facebook/posts/search",
            params={"q": q, "count": count},
            items_key="posts",
            cast_to=FacebookPost,
        ):
            yield item
