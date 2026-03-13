"""YouTube platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, YouTubeChannel, YouTubeComment, YouTubeVideo


class YouTube(APIResource):
    """Sync YouTube namespace."""

    def get_video(self, video_id: str) -> APIResponse[YouTubeVideo]:
        return self._get(f"/youtube/videos/{video_id}", cast_to=YouTubeVideo)

    def get_channel(self, channel_id: str) -> APIResponse[YouTubeChannel]:
        return self._get(f"/youtube/channels/{channel_id}", cast_to=YouTubeChannel)

    def search(
        self, q: str, *, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get("/youtube/search", params={"q": q, "count": count})

    def get_video_comments(
        self, video_id: str, *, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/youtube/videos/{video_id}/comments", params={"count": count}
        )

    def get_video_transcription(
        self, video_id: str, *, language: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/youtube/videos/{video_id}/transcription", params={"language": language}
        )

    # -- Auto-pagination iterators --

    def iter_search(
        self, q: str, *, count: int | None = None
    ) -> Iterator[YouTubeVideo]:
        return self._paginate(
            "/youtube/search",
            params={"q": q, "count": count},
            items_key="videos",
            cast_to=YouTubeVideo,
        )

    def iter_video_comments(
        self, video_id: str, *, count: int | None = None
    ) -> Iterator[YouTubeComment]:
        return self._paginate(
            f"/youtube/videos/{video_id}/comments",
            params={"count": count},
            items_key="comments",
            cast_to=YouTubeComment,
        )


class AsyncYouTube(AsyncAPIResource):
    """Async YouTube namespace."""

    async def get_video(self, video_id: str) -> APIResponse[YouTubeVideo]:
        return await self._get(f"/youtube/videos/{video_id}", cast_to=YouTubeVideo)

    async def get_channel(self, channel_id: str) -> APIResponse[YouTubeChannel]:
        return await self._get(f"/youtube/channels/{channel_id}", cast_to=YouTubeChannel)

    async def search(
        self, q: str, *, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get("/youtube/search", params={"q": q, "count": count})

    async def get_video_comments(
        self, video_id: str, *, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/youtube/videos/{video_id}/comments", params={"count": count}
        )

    async def get_video_transcription(
        self, video_id: str, *, language: str | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/youtube/videos/{video_id}/transcription", params={"language": language}
        )

    # -- Auto-pagination iterators --

    async def iter_search(
        self, q: str, *, count: int | None = None
    ) -> AsyncIterator[YouTubeVideo]:
        async for item in self._paginate(
            "/youtube/search",
            params={"q": q, "count": count},
            items_key="videos",
            cast_to=YouTubeVideo,
        ):
            yield item

    async def iter_video_comments(
        self, video_id: str, *, count: int | None = None
    ) -> AsyncIterator[YouTubeComment]:
        async for item in self._paginate(
            f"/youtube/videos/{video_id}/comments",
            params={"count": count},
            items_key="comments",
            cast_to=YouTubeComment,
        ):
            yield item
