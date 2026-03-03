"""Threads platform namespace."""

from __future__ import annotations

import time
from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import (
    APIResponse,
    BulkJob,
    BulkJobStatus,
    ThreadsPost,
    ThreadsUser,
)


class Threads(APIResource):
    """Sync Threads namespace."""

    def get_post(self, post_id: str, *, mode: str | None = None) -> APIResponse[ThreadsPost]:
        return self._get(f"/threads/posts/{post_id}", params={"mode": mode}, cast_to=ThreadsPost)

    def get_posts(
        self, ids: list[str], *, mode: str | None = None
    ) -> APIResponse[list[ThreadsPost]]:
        return self._get(
            "/threads/posts",
            params={"ids": ",".join(ids), "mode": mode},
            cast_to=ThreadsPost,
        )

    def search_posts(
        self, q: str, *, count: int | None = None
    ) -> APIResponse[list[ThreadsPost]]:
        return self._get(
            "/threads/posts/search", params={"q": q, "count": count}, cast_to=ThreadsPost,
            items_key="posts",
        )

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
        return self._get(
            "/threads/users/search", params={"q": q, "count": count}, cast_to=ThreadsUser
        )

    def get_public_feed(
        self, *, cursor: str | None = None, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return self._get("/threads/feed/public", params={"cursor": cursor, "count": count})

    # -- Bulk operations --

    def bulk_submit(self, ids: list[str]) -> APIResponse[BulkJob]:
        return self._post("/threads/bulk", body={"ids": ids}, cast_to=BulkJob)

    def bulk_status(self, job_id: str) -> APIResponse[BulkJobStatus]:
        return self._get(f"/threads/bulk/{job_id}", cast_to=BulkJobStatus)

    def bulk_results(self, job_id: str) -> APIResponse[list[ThreadsPost]]:
        return self._get(f"/threads/bulk/{job_id}/results", cast_to=ThreadsPost)

    def bulk_submit_and_wait(
        self,
        ids: list[str],
        *,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> APIResponse[list[ThreadsPost]]:
        """Submit a bulk job and poll until completion."""
        submit_resp = self.bulk_submit(ids)
        job_id = submit_resp.data.job_id  # type: ignore[union-attr]
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            status_resp = self.bulk_status(job_id)
            status = status_resp.data.status  # type: ignore[union-attr]
            if status == "completed":
                return self.bulk_results(job_id)
            if status == "failed":
                from .._exceptions import ByCrawlError

                raise ByCrawlError(f"Bulk job {job_id} failed")
            time.sleep(poll_interval)
        from .._exceptions import TimeoutError

        raise TimeoutError(f"Bulk job {job_id} timed out after {timeout}s")

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
        self, post_id: str, *, mode: str | None = None
    ) -> APIResponse[ThreadsPost]:
        return await self._get(
            f"/threads/posts/{post_id}", params={"mode": mode}, cast_to=ThreadsPost
        )

    async def get_posts(
        self, ids: list[str], *, mode: str | None = None
    ) -> APIResponse[list[ThreadsPost]]:
        return await self._get(
            "/threads/posts",
            params={"ids": ",".join(ids), "mode": mode},
            cast_to=ThreadsPost,
        )

    async def search_posts(
        self, q: str, *, count: int | None = None
    ) -> APIResponse[list[ThreadsPost]]:
        return await self._get(
            "/threads/posts/search", params={"q": q, "count": count}, cast_to=ThreadsPost,
            items_key="posts",
        )

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
        return await self._get(
            "/threads/users/search", params={"q": q, "count": count}, cast_to=ThreadsUser
        )

    async def get_public_feed(
        self, *, cursor: str | None = None, count: int | None = None
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            "/threads/feed/public", params={"cursor": cursor, "count": count}
        )

    # -- Bulk operations --

    async def bulk_submit(self, ids: list[str]) -> APIResponse[BulkJob]:
        return await self._post("/threads/bulk", body={"ids": ids}, cast_to=BulkJob)

    async def bulk_status(self, job_id: str) -> APIResponse[BulkJobStatus]:
        return await self._get(f"/threads/bulk/{job_id}", cast_to=BulkJobStatus)

    async def bulk_results(self, job_id: str) -> APIResponse[list[ThreadsPost]]:
        return await self._get(f"/threads/bulk/{job_id}/results", cast_to=ThreadsPost)

    async def bulk_submit_and_wait(
        self,
        ids: list[str],
        *,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> APIResponse[list[ThreadsPost]]:
        """Submit a bulk job and poll until completion."""
        import asyncio

        submit_resp = await self.bulk_submit(ids)
        job_id = submit_resp.data.job_id  # type: ignore[union-attr]
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            status_resp = await self.bulk_status(job_id)
            status = status_resp.data.status  # type: ignore[union-attr]
            if status == "completed":
                return await self.bulk_results(job_id)
            if status == "failed":
                from .._exceptions import ByCrawlError

                raise ByCrawlError(f"Bulk job {job_id} failed")
            await asyncio.sleep(poll_interval)
        from .._exceptions import TimeoutError

        raise TimeoutError(f"Bulk job {job_id} timed out after {timeout}s")

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
