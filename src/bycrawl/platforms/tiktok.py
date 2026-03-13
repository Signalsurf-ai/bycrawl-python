"""TikTok platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, TikTokComment, TikTokUser, TikTokVideo


class TikTok(APIResource):
    """Sync TikTok namespace."""

    def get_video(self, video_id: str) -> APIResponse[TikTokVideo]:
        return self._get(f"/tiktok/videos/{video_id}", cast_to=TikTokVideo)

    def get_user(self, username: str) -> APIResponse[TikTokUser]:
        return self._get(f"/tiktok/users/{username}", cast_to=TikTokUser)

    def get_user_videos(
        self, username: str, *, count: int | None = None
    ) -> APIResponse[list[TikTokVideo]]:
        return self._get(
            f"/tiktok/users/{username}/videos",
            params={"count": count},
            cast_to=TikTokVideo,
        )

    def get_video_comments(
        self, video_id: str, *, cursor: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/tiktok/videos/{video_id}/comments", params={"cursor": cursor}
        )

    def get_categories(
        self, *, category: str | None = None, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/tiktok/categories", params={"category": category, "count": count}
        )

    def search(
        self, keyword: str, *, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            "/tiktok/search", params={"keyword": keyword, "count": count}
        )

    def get_video_subtitles(
        self, video_id: str
    ) -> APIResponse[dict[str, Any]]:
        return self._get(f"/tiktok/videos/{video_id}/subtitles")

    # -- Auto-pagination iterators --

    def iter_video_comments(self, video_id: str) -> Iterator[TikTokComment]:
        return self._paginate(
            f"/tiktok/videos/{video_id}/comments",
            params={},
            items_key="comments",
            cast_to=TikTokComment,
        )


class AsyncTikTok(AsyncAPIResource):
    """Async TikTok namespace."""

    async def get_video(self, video_id: str) -> APIResponse[TikTokVideo]:
        return await self._get(f"/tiktok/videos/{video_id}", cast_to=TikTokVideo)

    async def get_user(self, username: str) -> APIResponse[TikTokUser]:
        return await self._get(f"/tiktok/users/{username}", cast_to=TikTokUser)

    async def get_user_videos(
        self, username: str, *, count: int | None = None
    ) -> APIResponse[list[TikTokVideo]]:
        return await self._get(
            f"/tiktok/users/{username}/videos",
            params={"count": count},
            cast_to=TikTokVideo,
        )

    async def get_video_comments(
        self, video_id: str, *, cursor: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/tiktok/videos/{video_id}/comments", params={"cursor": cursor}
        )

    async def get_categories(
        self, *, category: str | None = None, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/tiktok/categories", params={"category": category, "count": count}
        )

    async def search(
        self, keyword: str, *, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/tiktok/search", params={"keyword": keyword, "count": count}
        )

    async def get_video_subtitles(
        self, video_id: str
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/tiktok/videos/{video_id}/subtitles")

    # -- Auto-pagination iterators --

    async def iter_video_comments(
        self, video_id: str
    ) -> AsyncIterator[TikTokComment]:
        async for item in self._paginate(
            f"/tiktok/videos/{video_id}/comments",
            params={},
            items_key="comments",
            cast_to=TikTokComment,
        ):
            yield item
