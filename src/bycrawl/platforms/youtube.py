"""YouTube platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, YouTubeChannel, YouTubeVideo


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
