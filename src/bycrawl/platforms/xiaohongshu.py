"""Xiaohongshu (Little Red Book) platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import (
    APIResponse,
    XiaohongshuComment,
    XiaohongshuNote,
    XiaohongshuUser,
)


class Xiaohongshu(APIResource):
    """Sync Xiaohongshu namespace."""

    def search_notes(
        self, q: str, *, sort: str | None = None
    ) -> APIResponse[list[XiaohongshuNote]]:
        return self._get(
            "/xiaohongshu/notes/search",
            params={"keyword": q, "sort": sort},
            cast_to=XiaohongshuNote,
            items_key="notes",
        )

    def get_note(self, note_id: str) -> APIResponse[XiaohongshuNote]:
        return self._get(f"/xiaohongshu/notes/{note_id}", cast_to=XiaohongshuNote)

    def get_note_comments(self, note_id: str) -> APIResponse[list[XiaohongshuComment]]:
        return self._get(
            f"/xiaohongshu/notes/{note_id}/comments", cast_to=XiaohongshuComment
        )

    def get_comment_replies(
        self,
        note_id: str,
        comment_id: str,
        *,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/xiaohongshu/notes/{note_id}/comments/{comment_id}/replies",
            params={"cursor": cursor},
        )

    def search_users(self, q: str) -> APIResponse[list[XiaohongshuUser]]:
        return self._get(
            "/xiaohongshu/users/search", params={"keyword": q}, cast_to=XiaohongshuUser
        )

    def get_user(self, user_id: str) -> APIResponse[XiaohongshuUser]:
        return self._get(f"/xiaohongshu/users/{user_id}", cast_to=XiaohongshuUser)

    def get_user_notes(self, user_id: str) -> APIResponse[list[XiaohongshuNote]]:
        return self._get(f"/xiaohongshu/users/{user_id}/notes", cast_to=XiaohongshuNote)

    def get_feed(self, *, category: str | None = None) -> APIResponse[dict[str, Any]]:
        return self._get("/xiaohongshu/feed", params={"category": category})

    def resolve_share_url(self, url: str) -> APIResponse[dict[str, Any]]:
        return self._get("/xiaohongshu/share/resolve", params={"url": url})

    # -- Auto-pagination iterators --

    def iter_search_notes(
        self, q: str, *, sort: str | None = None
    ) -> Iterator[XiaohongshuNote]:
        return self._paginate_by_page(
            "/xiaohongshu/notes/search",
            params={"keyword": q, "sort": sort},
            items_key="notes",
            cast_to=XiaohongshuNote,
        )

    def iter_note_comments(self, note_id: str) -> Iterator[XiaohongshuComment]:
        return self._paginate(
            f"/xiaohongshu/notes/{note_id}/comments",
            params={},
            items_key="comments",
            cast_to=XiaohongshuComment,
        )

    def iter_user_notes(self, user_id: str) -> Iterator[XiaohongshuNote]:
        return self._paginate(
            f"/xiaohongshu/users/{user_id}/notes",
            params={},
            items_key="notes",
            cast_to=XiaohongshuNote,
        )


class AsyncXiaohongshu(AsyncAPIResource):
    """Async Xiaohongshu namespace."""

    async def search_notes(
        self, q: str, *, sort: str | None = None
    ) -> APIResponse[list[XiaohongshuNote]]:
        return await self._get(
            "/xiaohongshu/notes/search",
            params={"keyword": q, "sort": sort},
            cast_to=XiaohongshuNote,
            items_key="notes",
        )

    async def get_note(self, note_id: str) -> APIResponse[XiaohongshuNote]:
        return await self._get(f"/xiaohongshu/notes/{note_id}", cast_to=XiaohongshuNote)

    async def get_note_comments(
        self, note_id: str
    ) -> APIResponse[list[XiaohongshuComment]]:
        return await self._get(
            f"/xiaohongshu/notes/{note_id}/comments", cast_to=XiaohongshuComment
        )

    async def get_comment_replies(
        self,
        note_id: str,
        comment_id: str,
        *,
        cursor: str | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/xiaohongshu/notes/{note_id}/comments/{comment_id}/replies",
            params={"cursor": cursor},
        )

    async def search_users(self, q: str) -> APIResponse[list[XiaohongshuUser]]:
        return await self._get(
            "/xiaohongshu/users/search", params={"keyword": q}, cast_to=XiaohongshuUser
        )

    async def get_user(self, user_id: str) -> APIResponse[XiaohongshuUser]:
        return await self._get(f"/xiaohongshu/users/{user_id}", cast_to=XiaohongshuUser)

    async def get_user_notes(
        self, user_id: str
    ) -> APIResponse[list[XiaohongshuNote]]:
        return await self._get(
            f"/xiaohongshu/users/{user_id}/notes", cast_to=XiaohongshuNote
        )

    async def get_feed(
        self, *, category: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get("/xiaohongshu/feed", params={"category": category})

    async def resolve_share_url(self, url: str) -> APIResponse[dict[str, Any]]:
        return await self._get("/xiaohongshu/share/resolve", params={"url": url})

    # -- Auto-pagination iterators --

    async def iter_search_notes(
        self, q: str, *, sort: str | None = None
    ) -> AsyncIterator[XiaohongshuNote]:
        async for item in self._paginate_by_page(
            "/xiaohongshu/notes/search",
            params={"keyword": q, "sort": sort},
            items_key="notes",
            cast_to=XiaohongshuNote,
        ):
            yield item

    async def iter_note_comments(
        self, note_id: str
    ) -> AsyncIterator[XiaohongshuComment]:
        async for item in self._paginate(
            f"/xiaohongshu/notes/{note_id}/comments",
            params={},
            items_key="comments",
            cast_to=XiaohongshuComment,
        ):
            yield item

    async def iter_user_notes(
        self, user_id: str
    ) -> AsyncIterator[XiaohongshuNote]:
        async for item in self._paginate(
            f"/xiaohongshu/users/{user_id}/notes",
            params={},
            items_key="notes",
            cast_to=XiaohongshuNote,
        ):
            yield item
