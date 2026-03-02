"""
ByCrawl Client

ByCrawl (sync) and AsyncByCrawl (async) are the main entry points for the SDK.
Each client wires up all platform namespaces and manages the HTTP transport.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from ._http import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    AsyncTransport,
    SyncTransport,
)
from .platforms.facebook import AsyncFacebook, Facebook
from .platforms.instagram import AsyncInstagram, Instagram
from .platforms.job104 import AsyncJob104, Job104
from .platforms.linkedin import AsyncLinkedIn, LinkedIn
from .platforms.reddit import AsyncReddit, Reddit
from .platforms.threads import AsyncThreads, Threads
from .platforms.tiktok import AsyncTikTok, TikTok
from .platforms.x import AsyncX, X
from .platforms.xiaohongshu import AsyncXiaohongshu, Xiaohongshu


class ByCrawl:
    """Synchronous ByCrawl client.

    Usage::

        client = ByCrawl(api_key="sk_byc_...")
        post = client.threads.get_post("DQt-ox3kdE4")
        print(post.data)

    Or as a context manager::

        with ByCrawl(api_key="sk_byc_...") as client:
            user = client.threads.get_user("zuck")
    """

    threads: Threads
    facebook: Facebook
    x: X
    instagram: Instagram
    reddit: Reddit
    linkedin: LinkedIn
    xiaohongshu: Xiaohongshu
    tiktok: TikTok
    job104: Job104

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.Client | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("BYCRAWL_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "api_key must be provided or set via the BYCRAWL_API_KEY environment variable"
            )

        self._transport = SyncTransport(
            api_key=resolved_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )

        self.threads = Threads(self._transport)
        self.facebook = Facebook(self._transport)
        self.x = X(self._transport)
        self.instagram = Instagram(self._transport)
        self.reddit = Reddit(self._transport)
        self.linkedin = LinkedIn(self._transport)
        self.xiaohongshu = Xiaohongshu(self._transport)
        self.tiktok = TikTok(self._transport)
        self.job104 = Job104(self._transport)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self) -> ByCrawl:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncByCrawl:
    """Asynchronous ByCrawl client.

    Usage::

        async with AsyncByCrawl(api_key="sk_byc_...") as client:
            post = await client.threads.get_post("DQt-ox3kdE4")
            print(post.data)
    """

    threads: AsyncThreads
    facebook: AsyncFacebook
    x: AsyncX
    instagram: AsyncInstagram
    reddit: AsyncReddit
    linkedin: AsyncLinkedIn
    xiaohongshu: AsyncXiaohongshu
    tiktok: AsyncTikTok
    job104: AsyncJob104

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("BYCRAWL_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "api_key must be provided or set via the BYCRAWL_API_KEY environment variable"
            )

        self._transport = AsyncTransport(
            api_key=resolved_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
        )

        self.threads = AsyncThreads(self._transport)
        self.facebook = AsyncFacebook(self._transport)
        self.x = AsyncX(self._transport)
        self.instagram = AsyncInstagram(self._transport)
        self.reddit = AsyncReddit(self._transport)
        self.linkedin = AsyncLinkedIn(self._transport)
        self.xiaohongshu = AsyncXiaohongshu(self._transport)
        self.tiktok = AsyncTikTok(self._transport)
        self.job104 = AsyncJob104(self._transport)

    async def close(self) -> None:
        await self._transport.close()

    async def __aenter__(self) -> AsyncByCrawl:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
