"""Job104 (104人力銀行) platform namespace."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, Job104Company, Job104Job


class Job104(APIResource):
    """Sync Job104 namespace."""

    def search_jobs(
        self,
        *,
        q: str | None = None,
        welfare: str | None = None,
        area: str | None = None,
        page: int | None = None,
        count: int | None = None,
    ) -> APIResponse[list[Job104Job]]:
        return self._get_list(
            "/job104/jobs/search",
            params={
                "q": q,
                "welfare": welfare,
                "area": area,
                "page": page,
                "count": count,
            },
            items_key="jobs",
            cast_to=Job104Job,
        )

    def get_company(self, company_id: str) -> APIResponse[Job104Company]:
        return self._get(f"/job104/companies/{company_id}", cast_to=Job104Company)

    def get_job(self, job_id: str) -> APIResponse[Job104Job]:
        return self._get(f"/job104/jobs/{job_id}", cast_to=Job104Job)

    # -- Auto-pagination iterators --

    def iter_search_jobs(
        self,
        *,
        q: str | None = None,
        welfare: str | None = None,
        area: str | None = None,
        count: int | None = None,
    ) -> Iterator[Job104Job]:
        return self._paginate_by_page(
            "/job104/jobs/search",
            params={"q": q, "welfare": welfare, "area": area, "count": count or 20},
            items_key="jobs",
            page_key="page",
            cast_to=Job104Job,
        )


class AsyncJob104(AsyncAPIResource):
    """Async Job104 namespace."""

    async def search_jobs(
        self,
        *,
        q: str | None = None,
        welfare: str | None = None,
        area: str | None = None,
        page: int | None = None,
        count: int | None = None,
    ) -> APIResponse[list[Job104Job]]:
        return await self._get_list(
            "/job104/jobs/search",
            params={
                "q": q,
                "welfare": welfare,
                "area": area,
                "page": page,
                "count": count,
            },
            items_key="jobs",
            cast_to=Job104Job,
        )

    async def get_company(self, company_id: str) -> APIResponse[Job104Company]:
        return await self._get(f"/job104/companies/{company_id}", cast_to=Job104Company)

    async def get_job(self, job_id: str) -> APIResponse[Job104Job]:
        return await self._get(f"/job104/jobs/{job_id}", cast_to=Job104Job)

    # -- Auto-pagination iterators --

    async def iter_search_jobs(
        self,
        *,
        q: str | None = None,
        welfare: str | None = None,
        area: str | None = None,
        count: int | None = None,
    ) -> AsyncIterator[Job104Job]:
        async for item in self._paginate_by_page(
            "/job104/jobs/search",
            params={"q": q, "welfare": welfare, "area": area, "count": count or 20},
            items_key="jobs",
            page_key="page",
            cast_to=Job104Job,
        ):
            yield item
