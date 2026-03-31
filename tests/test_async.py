"""Tests for async client to verify async methods work correctly."""

from __future__ import annotations

import httpx
import pytest
import respx

from bycrawl import AsyncByCrawl
from bycrawl._types import ThreadsPost, ThreadsUser, XUser


@pytest.mark.asyncio
class TestAsyncThreads:
    @respx.mock(base_url="https://api.bycrawl.com")
    async def test_get_post(self, respx_mock: respx.Router):
        respx_mock.get("/threads/posts/abc").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "abc", "code": "xyz", "text": "hello"}
            })
        )
        async with AsyncByCrawl(api_key="sk_byc_test") as client:
            resp = await client.threads.get_post("abc")
            assert isinstance(resp.data, ThreadsPost)
            assert resp.data.id == "abc"

    @respx.mock(base_url="https://api.bycrawl.com")
    async def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/threads/users/zuck").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "1", "username": "zuck"}
            })
        )
        async with AsyncByCrawl(api_key="sk_byc_test") as client:
            resp = await client.threads.get_user("zuck")
            assert isinstance(resp.data, ThreadsUser)

    @respx.mock(base_url="https://api.bycrawl.com")
    async def test_search_posts(self, respx_mock: respx.Router):
        respx_mock.get("/threads/posts/search").mock(
            return_value=httpx.Response(200, json={
                "data": [{"id": "1", "code": "a", "text": "match"}]
            })
        )
        async with AsyncByCrawl(api_key="sk_byc_test") as client:
            resp = await client.threads.search_posts("test")
            assert len(resp.data) == 1

    @respx.mock(base_url="https://api.bycrawl.com")
    async def test_iter_user_posts(self, respx_mock: respx.Router):
        respx_mock.get("/threads/users/zuck/posts").mock(
            return_value=httpx.Response(200, json={
                "data": {
                    "posts": [{"id": "1", "code": "a", "text": "hello"}],
                    "hasMore": False,
                }
            })
        )
        async with AsyncByCrawl(api_key="sk_byc_test") as client:
            posts = []
            async for post in client.threads.iter_user_posts("zuck"):
                posts.append(post)
            assert len(posts) == 1
            assert isinstance(posts[0], ThreadsPost)


@pytest.mark.asyncio
class TestAsyncX:
    @respx.mock(base_url="https://api.bycrawl.com")
    async def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/x/users/test").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "1", "username": "test"}
            })
        )
        async with AsyncByCrawl(api_key="sk_byc_test") as client:
            resp = await client.x.get_user("test")
            assert isinstance(resp.data, XUser)


@pytest.mark.asyncio
class TestAsyncWebFetch:
    @respx.mock(base_url="https://api.bycrawl.com")
    async def test_fetch(self, respx_mock: respx.Router):
        respx_mock.get("/web/fetch").mock(
            return_value=httpx.Response(200, json={
                "data": {"content": "hello"}
            })
        )
        async with AsyncByCrawl(api_key="sk_byc_test") as client:
            resp = await client.web.fetch("https://example.com")
            assert resp.data["content"] == "hello"


@pytest.mark.asyncio
class TestAsyncContextManager:
    @respx.mock(base_url="https://api.bycrawl.com")
    async def test_aenter_aexit(self, respx_mock: respx.Router):
        client = AsyncByCrawl(api_key="sk_byc_test")
        async with client as c:
            assert c is client
        # After exit, transport should be closed
