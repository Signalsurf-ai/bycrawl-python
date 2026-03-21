"""PTT platform namespace."""

from __future__ import annotations

from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse


class PTT(APIResource):
    """Sync PTT namespace."""

    def get_board(self, board_name: str) -> APIResponse[dict[str, Any]]:
        return self._get(f"/ptt/boards/{board_name}")

    def get_board_posts(
        self,
        board_name: str,
        *,
        page: int | None = None,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/ptt/boards/{board_name}/posts",
            params={"page": page, "count": count},
        )

    def get_post(self, url: str) -> APIResponse[dict[str, Any]]:
        return self._get("/ptt/posts", params={"url": url})

    def search_posts(
        self,
        board_name: str,
        q: str,
        *,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/ptt/boards/{board_name}/search",
            params={"q": q, "count": count},
        )


class AsyncPTT(AsyncAPIResource):
    """Async PTT namespace."""

    async def get_board(self, board_name: str) -> APIResponse[dict[str, Any]]:
        return await self._get(f"/ptt/boards/{board_name}")

    async def get_board_posts(
        self,
        board_name: str,
        *,
        page: int | None = None,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/ptt/boards/{board_name}/posts",
            params={"page": page, "count": count},
        )

    async def get_post(self, url: str) -> APIResponse[dict[str, Any]]:
        return await self._get("/ptt/posts", params={"url": url})

    async def search_posts(
        self,
        board_name: str,
        q: str,
        *,
        count: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/ptt/boards/{board_name}/search",
            params={"q": q, "count": count},
        )
