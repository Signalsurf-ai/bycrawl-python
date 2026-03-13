"""X (Twitter) platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, XPost, XUser


class X(APIResource):
    """Sync X namespace."""

    def get_user(self, username: str) -> APIResponse[XUser]:
        return self._get(f"/x/users/{username}", cast_to=XUser)

    def get_user_posts(
        self,
        username: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/x/users/{username}/posts",
            params={"count": count, "cursor": cursor},
        )

    def get_post(self, post_id: str) -> APIResponse[XPost]:
        return self._get(f"/x/posts/{post_id}", cast_to=XPost)

    def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
        product: str | None = None,
    ) -> APIResponse[list[XPost]]:
        return self._get_list(
            "/x/posts/search",
            params={"q": q, "count": count, "cursor": cursor, "product": product},
            items_key="tweets",
            cast_to=XPost,
        )

    # -- Auto-pagination iterators --

    def iter_user_posts(
        self, username: str, *, count: int | None = None
    ) -> Iterator[XPost]:
        return self._paginate(
            f"/x/users/{username}/posts",
            params={"count": count},
            items_key="posts",
            cast_to=XPost,
        )

    def iter_search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        product: str | None = None,
    ) -> Iterator[XPost]:
        return self._paginate(
            "/x/posts/search",
            params={"q": q, "count": count, "product": product},
            items_key="posts",
            cast_to=XPost,
        )


class AsyncX(AsyncAPIResource):
    """Async X namespace."""

    async def get_user(self, username: str) -> APIResponse[XUser]:
        return await self._get(f"/x/users/{username}", cast_to=XUser)

    async def get_user_posts(
        self,
        username: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/x/users/{username}/posts",
            params={"count": count, "cursor": cursor},
        )

    async def get_post(self, post_id: str) -> APIResponse[XPost]:
        return await self._get(f"/x/posts/{post_id}", cast_to=XPost)

    async def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        cursor: str | None = None,
        product: str | None = None,
    ) -> APIResponse[list[XPost]]:
        return await self._get_list(
            "/x/posts/search",
            params={"q": q, "count": count, "cursor": cursor, "product": product},
            items_key="tweets",
            cast_to=XPost,
        )

    # -- Auto-pagination iterators --

    async def iter_user_posts(
        self, username: str, *, count: int | None = None
    ) -> AsyncIterator[XPost]:
        async for item in self._paginate(
            f"/x/users/{username}/posts",
            params={"count": count},
            items_key="posts",
            cast_to=XPost,
        ):
            yield item

    async def iter_search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        product: str | None = None,
    ) -> AsyncIterator[XPost]:
        async for item in self._paginate(
            "/x/posts/search",
            params={"q": q, "count": count, "product": product},
            items_key="posts",
            cast_to=XPost,
        ):
            yield item
