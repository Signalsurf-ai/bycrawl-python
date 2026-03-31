"""Tests for all platform namespaces (sync only — async mirrors sync logic)."""

from __future__ import annotations

import httpx
import respx

from bycrawl import ByCrawl
from bycrawl._types import (
    DcardForum,
    DcardPersona,
    FacebookPost,
    FacebookUser,
    GMapsPlace,
    InstagramUser,
    Job104Company,
    Job104Job,
    LinkedInCompany,
    LinkedInJob,
    LinkedInPost,
    LinkedInUser,
    RedditPost,
    RedditUser,
    Subreddit,
    ThreadsPost,
    ThreadsUser,
    TikTokUser,
    TikTokVideo,
    XPost,
    XUser,
    YouTubeChannel,
    YouTubeVideo,
)

# ---------------------------------------------------------------------------
# Threads
# ---------------------------------------------------------------------------


class TestThreads:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_post(self, respx_mock: respx.Router):
        respx_mock.get("/threads/posts/abc").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "abc", "code": "xyz", "text": "hello"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.threads.get_post("abc")
        assert resp.success is True
        assert isinstance(resp.data, ThreadsPost)
        assert resp.data.id == "abc"
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/threads/users/zuck").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "1", "username": "zuck", "full_name": "Mark"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.threads.get_user("zuck")
        assert isinstance(resp.data, ThreadsUser)
        assert resp.data.username == "zuck"
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_posts(self, respx_mock: respx.Router):
        respx_mock.get("/threads/posts/search").mock(
            return_value=httpx.Response(200, json={
                "data": [{"id": "1", "code": "a", "text": "match"}]
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.threads.search_posts("test")
        assert isinstance(resp.data, list)
        assert len(resp.data) == 1
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_users(self, respx_mock: respx.Router):
        respx_mock.get("/threads/users/search").mock(
            return_value=httpx.Response(200, json={
                "data": [{"id": "1", "username": "zuck"}]
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.threads.search_users("zuck")
        assert isinstance(resp.data[0], ThreadsUser)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user_posts(self, respx_mock: respx.Router):
        respx_mock.get("/threads/users/zuck/posts").mock(
            return_value=httpx.Response(200, json={
                "data": {"posts": [], "hasMore": False}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.threads.get_user_posts("zuck")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_public_feed(self, respx_mock: respx.Router):
        respx_mock.get("/threads/feed/public").mock(
            return_value=httpx.Response(200, json={
                "data": {"posts": [], "hasMore": False}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.threads.get_public_feed()
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_posts_batch(self, respx_mock: respx.Router):
        respx_mock.get("/threads/posts").mock(
            return_value=httpx.Response(200, json={
                "data": [
                    {"id": "1", "code": "a", "text": "p1"},
                    {"id": "2", "code": "b", "text": "p2"},
                ]
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.threads.get_posts(["1", "2"])
        assert len(resp.data) == 2
        client.close()


# ---------------------------------------------------------------------------
# X / Twitter
# ---------------------------------------------------------------------------


class TestX:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/x/users/elonmusk").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "1", "username": "elonmusk", "name": "Elon Musk"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.x.get_user("elonmusk")
        assert isinstance(resp.data, XUser)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_post(self, respx_mock: respx.Router):
        respx_mock.get("/x/posts/123").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "123", "text": "hello world"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.x.get_post("123")
        assert isinstance(resp.data, XPost)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_posts(self, respx_mock: respx.Router):
        respx_mock.get("/x/posts/search").mock(
            return_value=httpx.Response(200, json={
                "data": {"posts": [], "hasMore": False}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.x.search_posts("python", product="Latest")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user_posts(self, respx_mock: respx.Router):
        respx_mock.get("/x/users/test/posts").mock(
            return_value=httpx.Response(200, json={
                "data": {"posts": [], "cursor": None}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.x.get_user_posts("test")
        assert resp.success is True
        client.close()


# ---------------------------------------------------------------------------
# Facebook
# ---------------------------------------------------------------------------


class TestFacebook:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/facebook/users/meta").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "1", "name": "Meta", "username": "meta"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.facebook.get_user("meta")
        assert isinstance(resp.data, FacebookUser)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_post_by_url(self, respx_mock: respx.Router):
        respx_mock.get("/facebook/posts").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "fp1", "text": "hello"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.facebook.get_post(url="https://facebook.com/post/123")
        assert isinstance(resp.data, FacebookPost)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_marketplace_browse(self, respx_mock: respx.Router):
        respx_mock.get("/facebook/marketplace/listings").mock(
            return_value=httpx.Response(200, json={"data": {"listings": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.facebook.marketplace_browse("taipei", category="electronics")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_marketplace_search(self, respx_mock: respx.Router):
        respx_mock.get("/facebook/marketplace/search").mock(
            return_value=httpx.Response(200, json={"data": {"listings": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.facebook.marketplace_search("iphone")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_marketplace_item(self, respx_mock: respx.Router):
        respx_mock.get("/facebook/marketplace/items/abc").mock(
            return_value=httpx.Response(200, json={"data": {"id": "abc"}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.facebook.marketplace_item("abc")
        assert resp.success is True
        client.close()


# ---------------------------------------------------------------------------
# Instagram
# ---------------------------------------------------------------------------


class TestInstagram:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/instagram/users/instagram").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "1", "username": "instagram"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.instagram.get_user("instagram")
        assert isinstance(resp.data, InstagramUser)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_tags(self, respx_mock: respx.Router):
        respx_mock.get("/instagram/tags/search").mock(
            return_value=httpx.Response(200, json={"data": {"tags": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.instagram.search_tags("food")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_post(self, respx_mock: respx.Router):
        respx_mock.get("/instagram/posts/abc123").mock(
            return_value=httpx.Response(200, json={"data": {"id": "abc123"}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.instagram.get_post("abc123")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_post_comments(self, respx_mock: respx.Router):
        respx_mock.get("/instagram/posts/abc/comments").mock(
            return_value=httpx.Response(200, json={
                "data": {"comments": [], "hasMore": False}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.instagram.get_post_comments("abc")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user_posts(self, respx_mock: respx.Router):
        respx_mock.get("/instagram/users/test/posts").mock(
            return_value=httpx.Response(200, json={
                "data": {"posts": [], "cursor": None}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.instagram.get_user_posts("test")
        assert resp.success is True
        client.close()


# ---------------------------------------------------------------------------
# Reddit
# ---------------------------------------------------------------------------


class TestReddit:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_subreddit(self, respx_mock: respx.Router):
        respx_mock.get("/reddit/subreddits/python").mock(
            return_value=httpx.Response(200, json={
                "data": {"name": "python", "subscribers": 1000000}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.reddit.get_subreddit("python")
        assert isinstance(resp.data, Subreddit)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_subreddit_posts_with_time_filter(self, respx_mock: respx.Router):
        route = respx_mock.get("/reddit/subreddits/python/posts").mock(
            return_value=httpx.Response(200, json={
                "data": [{"id": "1", "title": "Test"}]
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        client.reddit.get_subreddit_posts("python", sort="top", t="week")
        assert "t=week" in str(route.calls[0].request.url)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_post(self, respx_mock: respx.Router):
        respx_mock.get("/reddit/posts/abc").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "abc", "title": "Test"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.reddit.get_post("abc")
        assert isinstance(resp.data, RedditPost)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/reddit/users/spez").mock(
            return_value=httpx.Response(200, json={
                "data": {"username": "spez", "link_karma": 100000}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.reddit.get_user("spez")
        assert isinstance(resp.data, RedditUser)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_posts(self, respx_mock: respx.Router):
        respx_mock.get("/reddit/posts/search").mock(
            return_value=httpx.Response(200, json={
                "data": [{"id": "1", "title": "Python tips"}]
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.reddit.search_posts("python")
        assert len(resp.data) == 1
        client.close()


# ---------------------------------------------------------------------------
# LinkedIn
# ---------------------------------------------------------------------------


class TestLinkedIn:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_company(self, respx_mock: respx.Router):
        respx_mock.get("/linkedin/companies/microsoft").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "1", "name": "Microsoft"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.linkedin.get_company("microsoft")
        assert isinstance(resp.data, LinkedInCompany)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_job(self, respx_mock: respx.Router):
        respx_mock.get("/linkedin/jobs/123").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "123", "title": "SWE"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.linkedin.get_job("123")
        assert isinstance(resp.data, LinkedInJob)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_jobs(self, respx_mock: respx.Router):
        respx_mock.get("/linkedin/jobs/search").mock(
            return_value=httpx.Response(200, json={
                "data": [{"id": "1", "title": "SWE"}]
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.linkedin.search_jobs("python", location="SF")
        assert len(resp.data) == 1
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_post(self, respx_mock: respx.Router):
        respx_mock.get("/linkedin/posts/p1").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "p1", "text": "hello"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.linkedin.get_post("p1")
        assert isinstance(resp.data, LinkedInPost)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/linkedin/users/johndoe").mock(
            return_value=httpx.Response(200, json={
                "data": {"username": "johndoe", "first_name": "John"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.linkedin.get_user("johndoe")
        assert isinstance(resp.data, LinkedInUser)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_users(self, respx_mock: respx.Router):
        respx_mock.get("/linkedin/users/search").mock(
            return_value=httpx.Response(200, json={
                "data": [{"username": "john", "first_name": "John"}]
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.linkedin.search_users("John")
        assert len(resp.data) == 1
        client.close()


# ---------------------------------------------------------------------------
# TikTok
# ---------------------------------------------------------------------------


class TestTikTok:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_video(self, respx_mock: respx.Router):
        respx_mock.get("/tiktok/videos/v1").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "v1", "description": "test"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.tiktok.get_video("v1")
        assert isinstance(resp.data, TikTokVideo)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user(self, respx_mock: respx.Router):
        respx_mock.get("/tiktok/users/test").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "1", "username": "test"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.tiktok.get_user("test")
        assert isinstance(resp.data, TikTokUser)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_user_videos(self, respx_mock: respx.Router):
        respx_mock.get("/tiktok/users/test/videos").mock(
            return_value=httpx.Response(200, json={
                "data": [{"id": "v1", "description": "test"}]
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.tiktok.get_user_videos("test")
        assert len(resp.data) == 1
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search(self, respx_mock: respx.Router):
        respx_mock.get("/tiktok/videos/search").mock(
            return_value=httpx.Response(200, json={"data": {"videos": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.tiktok.search("cat")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_video_subtitles(self, respx_mock: respx.Router):
        respx_mock.get("/tiktok/videos/v1/subtitles").mock(
            return_value=httpx.Response(200, json={"data": {"subtitles": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.tiktok.get_video_subtitles("v1")
        assert resp.success is True
        client.close()


# ---------------------------------------------------------------------------
# YouTube
# ---------------------------------------------------------------------------


class TestYouTube:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_video(self, respx_mock: respx.Router):
        respx_mock.get("/youtube/videos/abc").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "abc", "title": "Test Video"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.youtube.get_video("abc")
        assert isinstance(resp.data, YouTubeVideo)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_channel(self, respx_mock: respx.Router):
        respx_mock.get("/youtube/channels/ch1").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "ch1", "title": "My Channel"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.youtube.get_channel("ch1")
        assert isinstance(resp.data, YouTubeChannel)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search(self, respx_mock: respx.Router):
        respx_mock.get("/youtube/videos/search").mock(
            return_value=httpx.Response(200, json={"data": {"videos": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.youtube.search("python tutorial")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_video_comments(self, respx_mock: respx.Router):
        respx_mock.get("/youtube/videos/abc/comments").mock(
            return_value=httpx.Response(200, json={
                "data": {"comments": []}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.youtube.get_video_comments("abc")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_video_transcription(self, respx_mock: respx.Router):
        respx_mock.get("/youtube/videos/abc/transcription").mock(
            return_value=httpx.Response(200, json={
                "data": {"text": "hello world"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.youtube.get_video_transcription("abc", language="en")
        assert resp.success is True
        client.close()


# ---------------------------------------------------------------------------
# Dcard
# ---------------------------------------------------------------------------


class TestDcard:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_forum(self, respx_mock: respx.Router):
        respx_mock.get("/dcard/forums/funny").mock(
            return_value=httpx.Response(200, json={
                "data": {"alias": "funny", "name": "Funny"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.dcard.get_forum("funny")
        assert isinstance(resp.data, DcardForum)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_forum_posts(self, respx_mock: respx.Router):
        respx_mock.get("/dcard/forums/funny/posts").mock(
            return_value=httpx.Response(200, json={"data": {"posts": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.dcard.get_forum_posts("funny", popular=True)
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_posts(self, respx_mock: respx.Router):
        respx_mock.get("/dcard/posts/search").mock(
            return_value=httpx.Response(200, json={"data": {"posts": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.dcard.search_posts("test")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_persona(self, respx_mock: respx.Router):
        respx_mock.get("/dcard/personas/test").mock(
            return_value=httpx.Response(200, json={
                "data": {"username": "test", "nickname": "T"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.dcard.get_persona("test")
        assert isinstance(resp.data, DcardPersona)
        client.close()


# ---------------------------------------------------------------------------
# Google Maps
# ---------------------------------------------------------------------------


class TestGMaps:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search(self, respx_mock: respx.Router):
        respx_mock.get("/gmaps/places/search").mock(
            return_value=httpx.Response(200, json={"data": {"places": []}})
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.gmaps.search("coffee taipei")
        assert resp.success is True
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_place(self, respx_mock: respx.Router):
        respx_mock.get("/gmaps/places").mock(
            return_value=httpx.Response(200, json={
                "data": {"name": "Cafe", "rating": 4.5}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.gmaps.get_place("Cafe Taipei", language="zh-TW")
        assert isinstance(resp.data, GMapsPlace)
        client.close()


# ---------------------------------------------------------------------------
# Job104
# ---------------------------------------------------------------------------


class TestJob104:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_search_jobs(self, respx_mock: respx.Router):
        respx_mock.get("/job104/jobs/search").mock(
            return_value=httpx.Response(200, json={
                "jobs": [
                    {"jobId": "1", "jobName": "SWE", "companyName": "Acme", "area": "Taipei"}
                ],
                "totalCount": 1,
                "page": 1,
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.job104.search_jobs(q="python")
        assert len(resp.data) == 1
        assert isinstance(resp.data[0], Job104Job)
        assert resp.data[0].id == "1"
        assert resp.data[0].title == "SWE"
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_job(self, respx_mock: respx.Router):
        respx_mock.get("/job104/jobs/123").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "123", "title": "Engineer"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.job104.get_job("123")
        assert isinstance(resp.data, Job104Job)
        client.close()

    @respx.mock(base_url="https://api.bycrawl.com")
    def test_get_company(self, respx_mock: respx.Router):
        respx_mock.get("/job104/companies/c1").mock(
            return_value=httpx.Response(200, json={
                "data": {"id": "c1", "name": "Acme"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.job104.get_company("c1")
        assert isinstance(resp.data, Job104Company)
        client.close()


# ---------------------------------------------------------------------------
# WebFetch
# ---------------------------------------------------------------------------


class TestWebFetch:
    @respx.mock(base_url="https://api.bycrawl.com")
    def test_fetch(self, respx_mock: respx.Router):
        respx_mock.get("/web/fetch").mock(
            return_value=httpx.Response(200, json={
                "data": {"content": "<html>hello</html>"}
            })
        )
        client = ByCrawl(api_key="sk_byc_test")
        resp = client.web.fetch("https://example.com")
        assert resp.success is True
        assert resp.data["content"] == "<html>hello</html>"
        client.close()
