"""Dcard platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, DcardForum, DcardPersona, DcardPost


class Dcard(APIResource):
    """Sync Dcard namespace."""

    def get_forum(self, alias: str) -> APIResponse[DcardForum]:
        return self._get(f"/dcard/forums/{alias}", cast_to=DcardForum)

    def get_forum_posts(
        self,
        alias: str,
        *,
        count: int | None = None,
        popular: bool | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/dcard/forums/{alias}/posts",
            params={"count": count, "popular": popular},
        )

    def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        offset: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/dcard/posts/search",
            params={"q": q, "count": count, "offset": offset},
        )

    def get_persona(self, username: str) -> APIResponse[DcardPersona]:
        return self._get(f"/dcard/personas/{username}", cast_to=DcardPersona)

    # -- Auto-pagination iterators --

    def iter_search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
    ) -> Iterator[DcardPost]:
        return self._paginate_by_offset(
            "/dcard/posts/search",
            params={"q": q, "count": count or 30},
            items_key="posts",
            cast_to=DcardPost,
        )


class AsyncDcard(AsyncAPIResource):
    """Async Dcard namespace."""

    async def get_forum(self, alias: str) -> APIResponse[DcardForum]:
        return await self._get(f"/dcard/forums/{alias}", cast_to=DcardForum)

    async def get_forum_posts(
        self,
        alias: str,
        *,
        count: int | None = None,
        popular: bool | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/dcard/forums/{alias}/posts",
            params={"count": count, "popular": popular},
        )

    async def search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
        offset: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/dcard/posts/search",
            params={"q": q, "count": count, "offset": offset},
        )

    async def get_persona(self, username: str) -> APIResponse[DcardPersona]:
        return await self._get(f"/dcard/personas/{username}", cast_to=DcardPersona)

    # -- Auto-pagination iterators --

    async def iter_search_posts(
        self,
        q: str,
        *,
        count: int | None = None,
    ) -> AsyncIterator[DcardPost]:
        async for item in self._paginate_by_offset(
            "/dcard/posts/search",
            params={"q": q, "count": count or 30},
            items_key="posts",
            cast_to=DcardPost,
        ):
            yield item
