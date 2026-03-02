"""LinkedIn platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._resource import APIResource, AsyncAPIResource
from .._types import (
    APIResponse,
    LinkedInCompany,
    LinkedInJob,
    LinkedInPost,
    LinkedInUser,
)


class LinkedIn(APIResource):
    """Sync LinkedIn namespace."""

    def get_company(self, company_id: str) -> APIResponse[LinkedInCompany]:
        return self._get(f"/linkedin/companies/{company_id}", cast_to=LinkedInCompany)

    def get_company_jobs(
        self,
        company_id: str,
        *,
        count: int | None = None,
        offset: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return self._get(
            f"/linkedin/companies/{company_id}/jobs",
            params={"count": count, "offset": offset},
        )

    def search_jobs(
        self,
        q: str,
        *,
        location: str | None = None,
        count: int | None = None,
    ) -> APIResponse[list[LinkedInJob]]:
        return self._get(
            "/linkedin/jobs/search",
            params={"q": q, "location": location, "count": count},
            cast_to=LinkedInJob,
        )

    def get_job(self, job_id: str) -> APIResponse[LinkedInJob]:
        return self._get(f"/linkedin/jobs/{job_id}", cast_to=LinkedInJob)

    def get_post(self, post_id: str) -> APIResponse[LinkedInPost]:
        return self._get(f"/linkedin/posts/{post_id}", cast_to=LinkedInPost)

    def search_users(
        self,
        query: str,
        *,
        count: int | None = None,
        offset: int | None = None,
    ) -> APIResponse[list[LinkedInUser]]:
        return self._get(
            "/linkedin/users/search",
            params={"query": query, "count": count, "offset": offset},
            cast_to=LinkedInUser,
        )

    def get_user(self, username: str) -> APIResponse[LinkedInUser]:
        return self._get(f"/linkedin/users/{username}", cast_to=LinkedInUser)

    # -- Auto-pagination iterators --

    def iter_company_jobs(
        self, company_id: str, *, count: int | None = None
    ) -> Iterator[LinkedInJob]:
        return self._paginate_by_offset(
            f"/linkedin/companies/{company_id}/jobs",
            params={"count": count or 10, "limit": count or 10},
            items_key="jobs",
            cast_to=LinkedInJob,
        )

    def iter_search_jobs(
        self,
        q: str,
        *,
        location: str | None = None,
        count: int | None = None,
    ) -> Iterator[LinkedInJob]:
        return self._paginate_by_offset(
            "/linkedin/jobs/search",
            params={"q": q, "location": location, "count": count or 10, "limit": count or 10},
            items_key="jobs",
            cast_to=LinkedInJob,
        )


class AsyncLinkedIn(AsyncAPIResource):
    """Async LinkedIn namespace."""

    async def get_company(self, company_id: str) -> APIResponse[LinkedInCompany]:
        return await self._get(f"/linkedin/companies/{company_id}", cast_to=LinkedInCompany)

    async def get_company_jobs(
        self,
        company_id: str,
        *,
        count: int | None = None,
        offset: int | None = None,
    ) -> APIResponse[dict[str, Any]]:
        return await self._get(
            f"/linkedin/companies/{company_id}/jobs",
            params={"count": count, "offset": offset},
        )

    async def search_jobs(
        self,
        q: str,
        *,
        location: str | None = None,
        count: int | None = None,
    ) -> APIResponse[list[LinkedInJob]]:
        return await self._get(
            "/linkedin/jobs/search",
            params={"q": q, "location": location, "count": count},
            cast_to=LinkedInJob,
        )

    async def get_job(self, job_id: str) -> APIResponse[LinkedInJob]:
        return await self._get(f"/linkedin/jobs/{job_id}", cast_to=LinkedInJob)

    async def get_post(self, post_id: str) -> APIResponse[LinkedInPost]:
        return await self._get(f"/linkedin/posts/{post_id}", cast_to=LinkedInPost)

    async def search_users(
        self,
        query: str,
        *,
        count: int | None = None,
        offset: int | None = None,
    ) -> APIResponse[list[LinkedInUser]]:
        return await self._get(
            "/linkedin/users/search",
            params={"query": query, "count": count, "offset": offset},
            cast_to=LinkedInUser,
        )

    async def get_user(self, username: str) -> APIResponse[LinkedInUser]:
        return await self._get(f"/linkedin/users/{username}", cast_to=LinkedInUser)

    # -- Auto-pagination iterators --

    async def iter_company_jobs(
        self, company_id: str, *, count: int | None = None
    ) -> AsyncIterator[LinkedInJob]:
        async for item in self._paginate_by_offset(
            f"/linkedin/companies/{company_id}/jobs",
            params={"count": count or 10, "limit": count or 10},
            items_key="jobs",
            cast_to=LinkedInJob,
        ):
            yield item

    async def iter_search_jobs(
        self,
        q: str,
        *,
        location: str | None = None,
        count: int | None = None,
    ) -> AsyncIterator[LinkedInJob]:
        async for item in self._paginate_by_offset(
            "/linkedin/jobs/search",
            params={"q": q, "location": location, "count": count or 10, "limit": count or 10},
            items_key="jobs",
            cast_to=LinkedInJob,
        ):
            yield item
