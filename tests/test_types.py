"""Tests for Pydantic response types."""

from __future__ import annotations

from bycrawl._types import (
    APIResponse,
    CreditInfo,
    FacebookPost,
    FacebookUser,
    GMapsPlace,
    InstagramTag,
    InstagramUser,
    Job104Job,
    LinkedInCompany,
    LinkedInJob,
    LinkedInPost,
    LinkedInUser,
    PaginatedData,
    RateLimit,
    RedditPost,
    RedditUser,
    Subreddit,
    ThreadsMedia,
    ThreadsPost,
    ThreadsPostStats,
    ThreadsUser,
    TikTokCategory,
    TikTokComment,
    TikTokUser,
    TikTokVideo,
    XPost,
    XUser,
    YouTubeChannel,
    YouTubeComment,
    YouTubeVideo,
)


class TestAPIResponse:
    def test_success_response(self):
        resp = APIResponse(success=True, data={"foo": "bar"})
        assert resp.success is True
        assert resp.data == {"foo": "bar"}

    def test_error_response(self):
        resp = APIResponse(success=False, error="something went wrong")
        assert resp.success is False
        assert resp.error == "something went wrong"
        assert resp.data is None

    def test_rate_limit_and_credit(self):
        rl = RateLimit(limit=60, remaining=59, reset=1700000000.0)
        ci = CreditInfo(remaining=100, used=5)
        resp = APIResponse(success=True, rate_limit=rl, credit=ci)
        assert resp.rate_limit.limit == 60
        assert resp.credit.remaining == 100


class TestPaginatedData:
    def test_empty(self):
        pd = PaginatedData()
        assert pd.items == []
        assert pd.next_cursor is None

    def test_with_items(self):
        pd = PaginatedData(items=[1, 2, 3], next_cursor="abc")
        assert len(pd.items) == 3
        assert pd.next_cursor == "abc"


class TestThreadsTypes:
    def test_threads_user(self):
        u = ThreadsUser(id="123", username="zuck", full_name="Mark")
        assert u.id == "123"
        assert u.username == "zuck"
        assert u.is_verified is False

    def test_threads_post(self):
        p = ThreadsPost(id="p1", text="hello")
        assert p.id == "p1"
        assert p.media == []
        assert p.is_reply is False

    def test_threads_post_stats(self):
        s = ThreadsPostStats(likes=10, replies=2)
        assert s.likes == 10
        assert s.quotes == 0

    def test_threads_media(self):
        m = ThreadsMedia(index=0, type="image", url="https://example.com/img.jpg")
        assert m.type == "image"

    def test_extra_fields_allowed(self):
        u = ThreadsUser.model_validate(
            {"id": "1", "username": "test", "new_field": "val"}
        )
        assert u.id == "1"


class TestXTypes:
    def test_x_user(self):
        u = XUser(id="1", username="elonmusk")
        assert u.is_blue_verified is False

    def test_x_post(self):
        p = XPost(id="t1", text="test tweet")
        assert p.is_retweet is False
        assert p.media == []


class TestFacebookTypes:
    def test_facebook_user(self):
        u = FacebookUser(id="1", name="Page Name")
        assert u.category is None

    def test_facebook_post(self):
        p = FacebookPost(id="fp1", text="hello")
        assert p.media == []


class TestInstagramTypes:
    def test_instagram_user(self):
        u = InstagramUser(id="1", username="test", is_private=True)
        assert u.is_private is True

    def test_instagram_tag(self):
        t = InstagramTag(name="food", media_count=1000)
        assert t.media_count == 1000


class TestRedditTypes:
    def test_subreddit(self):
        s = Subreddit(name="python", subscribers=1000000)
        assert s.name == "python"

    def test_reddit_post(self):
        p = RedditPost(id="abc", title="Test Post", is_nsfw=True)
        assert p.is_nsfw is True

    def test_reddit_user(self):
        u = RedditUser(username="testuser", is_gold=True)
        assert u.is_gold is True


class TestLinkedInTypes:
    def test_company(self):
        c = LinkedInCompany(id="1", name="Acme")
        assert c.universal_name is None

    def test_job(self):
        j = LinkedInJob(id="1", title="SWE")
        assert j.employment_type is None

    def test_post(self):
        p = LinkedInPost(id="1", text="hello")
        assert p.likes_count is None

    def test_user(self):
        u = LinkedInUser(username="john", first_name="John")
        assert u.headline is None


class TestTikTokTypes:
    def test_video(self):
        v = TikTokVideo(id="1", description="test")
        assert v.duration is None

    def test_user(self):
        u = TikTokUser(id="1", username="test", verified=True)
        assert u.verified is True

    def test_comment(self):
        c = TikTokComment(id="1", text="nice")
        assert c.like_count is None

    def test_category(self):
        cat = TikTokCategory(id="1", name="Comedy")
        assert cat.name == "Comedy"


class TestYouTubeTypes:
    def test_video(self):
        v = YouTubeVideo(id="1", title="Test")
        assert v.keywords == []

    def test_channel(self):
        c = YouTubeChannel(id="1", title="Channel")
        assert c.country is None

    def test_comment(self):
        c = YouTubeComment(id="1", text="great", is_verified=True)
        assert c.is_verified is True


class TestGMapsTypes:
    def test_place(self):
        p = GMapsPlace(name="Cafe", rating=4.5, lat=25.0, lng=121.0)
        assert p.rating == 4.5


class TestJob104Types:
    def test_job(self):
        j = Job104Job(id="1", title="Engineer", requirements=["Python"])
        assert j.requirements == ["Python"]


