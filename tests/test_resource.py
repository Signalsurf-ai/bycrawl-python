"""Tests for APIResource base class (response wrapping, header parsing, pagination)."""

from __future__ import annotations

import httpx
import respx

from bycrawl import ByCrawl
from bycrawl._http import ResponseWrapper
from bycrawl._resource import _parse_credit, _parse_rate_limit, _wrap_response
from bycrawl._types import CreditInfo, RateLimit, ThreadsUser


class TestParseRateLimit:
    def test_parses_headers(self):
        rl = _parse_rate_limit({
            "x-ratelimit-limit": "60",
            "x-ratelimit-remaining": "59",
            "x-ratelimit-reset": "1700000000",
        })
        assert rl == RateLimit(limit=60, remaining=59, reset=1700000000.0)

    def test_returns_none_when_no_headers(self):
        assert _parse_rate_limit({}) is None

    def test_partial_headers(self):
        rl = _parse_rate_limit({"x-ratelimit-limit": "100"})
        assert rl.limit == 100
        assert rl.remaining is None


class TestParseCredit:
    def test_parses_headers(self):
        ci = _parse_credit({
            "x-credit-remaining": "95",
            "x-credit-used": "5",
        })
        assert ci == CreditInfo(remaining=95, used=5)

    def test_returns_none_when_no_headers(self):
        assert _parse_credit({}) is None


class TestWrapResponse:
    def test_wraps_dict_data(self):
        wrapper = ResponseWrapper(
            status_code=200,
            data={"data": {"id": "1", "username": "test"}, "success": True},
            headers={},
        )
        resp = _wrap_response(wrapper, cast_to=ThreadsUser)
        assert resp.success is True
        assert isinstance(resp.data, ThreadsUser)
        assert resp.data.id == "1"

    def test_wraps_list_data(self):
        wrapper = ResponseWrapper(
            status_code=200,
            data={
                "data": [
                    {"id": "1", "username": "a"},
                    {"id": "2", "username": "b"},
                ],
            },
            headers={},
        )
        resp = _wrap_response(wrapper, cast_to=ThreadsUser)
        assert isinstance(resp.data, list)
        assert len(resp.data) == 2
        assert resp.data[0].username == "a"

    def test_wraps_without_cast(self):
        wrapper = ResponseWrapper(
            status_code=200,
            data={"data": {"raw": "value"}},
            headers={},
        )
        resp = _wrap_response(wrapper)
        assert resp.data == {"raw": "value"}

    def test_includes_rate_limit_and_credit(self):
        wrapper = ResponseWrapper(
            status_code=200,
            data={"data": None},
            headers={
                "x-ratelimit-limit": "60",
                "x-ratelimit-remaining": "58",
                "x-credit-remaining": "100",
                "x-credit-used": "2",
            },
        )
        resp = _wrap_response(wrapper)
        assert resp.rate_limit.limit == 60
        assert resp.credit.remaining == 100


class TestPagination:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_cursor_pagination_single_page(self, respx_mock: respx.Router):
        respx_mock.get("/threads/users/zuck/posts").mock(
            return_value=httpx.Response(200, json={
                "data": {
                    "posts": [
                        {"id": "1", "code": "a", "text": "hello"},
                        {"id": "2", "code": "b", "text": "world"},
                    ],
                    "hasMore": False,
                }
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        posts = list(client.threads.iter_user_posts("zuck"))
        assert len(posts) == 2
        assert posts[0].id == "1"
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_cursor_pagination_multi_page(self, respx_mock: respx.Router):
        respx_mock.get("/threads/users/zuck/posts").mock(
            side_effect=[
                httpx.Response(200, json={
                    "data": {
                        "posts": [{"id": "1", "code": "a", "text": "p1"}],
                        "hasMore": True,
                        "cursor": "cur1",
                    }
                }),
                httpx.Response(200, json={
                    "data": {
                        "posts": [{"id": "2", "code": "b", "text": "p2"}],
                        "hasMore": False,
                    }
                }),
            ]
        )
        client = ByCrawl(api_key="sk_byc_test")
        posts = list(client.threads.iter_user_posts("zuck"))
        assert len(posts) == 2
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_page_pagination(self, respx_mock: respx.Router):
        respx_mock.get("/job104/jobs/search").mock(
            side_effect=[
                httpx.Response(200, json={
                    "data": {
                        "jobs": [
                            {"id": "1", "title": "SWE"},
                            {"id": "2", "title": "PM"},
                        ],
                        "hasMore": True,
                    }
                }),
                httpx.Response(200, json={
                    "data": {
                        "jobs": [],
                    }
                }),
            ]
        )
        client = ByCrawl(api_key="sk_byc_test")
        jobs = list(client.job104.iter_search_jobs(q="python"))
        assert len(jobs) == 2
        assert jobs[0].title == "SWE"
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_offset_pagination(self, respx_mock: respx.Router):
        respx_mock.get("/linkedin/jobs/search").mock(
            side_effect=[
                httpx.Response(200, json={
                    "data": {
                        "jobs": [{"id": "1", "title": "SWE"}],
                        "count": 2,
                    }
                }),
                httpx.Response(200, json={
                    "data": {
                        "jobs": [{"id": "2", "title": "PM"}],
                        "count": 2,
                    }
                }),
            ]
        )
        client = ByCrawl(api_key="sk_byc_test")
        jobs = list(client.linkedin.iter_search_jobs("python", count=1))
        assert len(jobs) == 2
        client.close()
