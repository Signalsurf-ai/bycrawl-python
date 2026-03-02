"""Facebook platform namespace."""

from __future__ import annotations

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


class AsyncFacebook(AsyncAPIResource):
    """Async Facebook namespace."""

    async def get_user(self, username: str) -> APIResponse[FacebookUser]:
        return await self._get(f"/facebook/users/{username}", cast_to=FacebookUser)

    async def get_user_posts(self, username: str) -> APIResponse[list[FacebookPost]]:
        return await self._get(f"/facebook/users/{username}/posts", cast_to=FacebookPost)

    async def get_post(self, *, url: str) -> APIResponse[FacebookPost]:
        return await self._get("/facebook/posts", params={"url": url}, cast_to=FacebookPost)

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
