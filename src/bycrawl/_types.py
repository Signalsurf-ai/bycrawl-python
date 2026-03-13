"""
ByCrawl Response Types

Pydantic v2 models for all API responses. Models use ``extra="allow"`` so
new fields returned by the API won't break existing code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

T = TypeVar("T")

# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------


class _Base(BaseModel):
    model_config = ConfigDict(extra="allow", alias_generator=to_camel, populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def _coerce_null_bools(cls, values: Any) -> Any:
        """Coerce null values to defaults for bool fields so the API
        returning ``"isVerified": null`` doesn't cause validation errors."""
        if not isinstance(values, dict):
            return values
        for name, field_info in cls.model_fields.items():
            if field_info.annotation is bool and field_info.default is not None:
                # Check both snake_case and camelCase keys
                for key in (name, to_camel(name)):
                    if key in values and values[key] is None:
                        values[key] = field_info.default
        return values


# ---------------------------------------------------------------------------
# Rate Limit / Credit Info (parsed from response headers)
# ---------------------------------------------------------------------------


@dataclass
class RateLimit:
    """Rate limit info extracted from response headers."""

    limit: int | None = None
    remaining: int | None = None
    reset: float | None = None


@dataclass
class CreditInfo:
    """Credit info extracted from response headers."""

    remaining: int | None = None
    used: int | None = None


# ---------------------------------------------------------------------------
# APIResponse wrapper
# ---------------------------------------------------------------------------


class APIResponse(BaseModel, Generic[T]):
    """Top-level API response wrapper."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool
    data: T | None = None
    error: str | None = None
    queued: bool = False
    rate_limit: RateLimit | None = None
    credit: CreditInfo | None = None


class PaginatedData(_Base, Generic[T]):
    """Generic paginated wrapper used by list endpoints."""

    items: list[T] = []
    next_cursor: str | None = None


# ---------------------------------------------------------------------------
# Threads
# ---------------------------------------------------------------------------


class ThreadsUser(_Base):
    id: str
    username: str
    full_name: str | None = None
    profile_pic: str | None = None
    bio: str | None = None
    is_verified: bool = False
    follower_count: int | None = None
    following_count: int | None = None


class ThreadsPostStats(_Base):
    likes: int = 0
    replies: int = 0
    quotes: int = 0
    reposts: int = 0
    shares: int = 0


class ThreadsMedia(_Base):
    index: int = 0
    type: str = ""
    url: str = ""
    width: int | None = None
    height: int | None = None


class ThreadsPost(_Base):
    id: str
    code: str | None = None
    text: str | None = None
    user: ThreadsUser | None = None
    media: list[ThreadsMedia] = []
    stats: ThreadsPostStats | None = None
    created_at: str | None = None
    views: int | None = None
    is_reply: bool = False
    reply_to: Any | None = None


# ---------------------------------------------------------------------------
# Facebook
# ---------------------------------------------------------------------------


class FacebookUser(_Base):
    id: str | None = None
    name: str | None = None
    username: str | None = None
    category: str | None = None
    profile_picture: str | None = None
    cover_photo: str | None = None
    likes_count: int | None = None
    description: str | None = None


class FacebookPost(_Base):
    id: str | None = None
    url: str | None = None
    text: str | None = None
    created_at: str | None = None
    reaction_count: int | None = None
    comment_count: int | None = None
    share_count: int | None = None
    view_count: int | None = None
    media: list[dict[str, Any]] = []


# ---------------------------------------------------------------------------
# X / Twitter
# ---------------------------------------------------------------------------


class XUser(_Base):
    id: str
    username: str
    name: str | None = None
    description: str | None = None
    profile_image_url: str | None = None
    banner_url: str | None = None
    followers_count: int | None = None
    following_count: int | None = None
    tweet_count: int | None = None
    is_verified: bool = False
    is_blue_verified: bool = False
    created_at: str | None = None
    location: str | None = None
    url: str | None = None


class XPost(_Base):
    id: str
    text: str | None = None
    created_at: str | None = None
    user: XUser | None = None
    like_count: int | None = None
    retweet_count: int | None = None
    reply_count: int | None = None
    quote_count: int | None = None
    bookmark_count: int | None = None
    view_count: int | None = None
    media: list[dict[str, Any]] = []
    is_retweet: bool = False
    is_reply: bool = False
    lang: str | None = None
    url: str | None = None


# ---------------------------------------------------------------------------
# Instagram
# ---------------------------------------------------------------------------


class InstagramUser(_Base):
    id: str | None = None
    username: str | None = None
    full_name: str | None = None
    biography: str | None = None
    profile_pic_url: str | None = None
    follower_count: int | None = None
    following_count: int | None = None
    media_count: int | None = None
    is_verified: bool = False
    is_private: bool = False


class InstagramTag(_Base):
    name: str | None = None
    media_count: int | None = None


# ---------------------------------------------------------------------------
# Reddit
# ---------------------------------------------------------------------------


class Subreddit(_Base):
    name: str | None = None
    title: str | None = None
    description: str | None = None
    subscribers: int | None = None
    active_users: int | None = None
    created_at: str | None = None


class RedditPost(_Base):
    id: str
    title: str | None = None
    text: str | None = None
    url: str | None = None
    author: str | None = None
    subreddit: str | None = None
    score: int | None = None
    upvote_ratio: float | None = None
    num_comments: int | None = Field(None, alias="commentCount")
    created_at: str | None = None
    permalink: str | None = None
    is_nsfw: bool = False


class RedditUser(_Base):
    username: str | None = None
    id: str | None = None
    created_at: str | None = None
    link_karma: int | None = None
    comment_karma: int | None = None
    is_gold: bool = False


# ---------------------------------------------------------------------------
# LinkedIn
# ---------------------------------------------------------------------------


class LinkedInCompany(_Base):
    id: str | None = None
    name: str | None = None
    universal_name: str | None = None
    description: str | None = None
    website: str | None = None
    industry: str | None = None
    company_size: str | None = Field(None, alias="size")
    headquarters: str | None = None
    logo_url: str | None = Field(None, alias="logo")
    banner: str | None = None
    employee_count: int | str | None = None
    follower_count: int | None = None
    specialties: list[str] | None = None
    founded: str | None = None


class LinkedInJob(_Base):
    id: str | None = None
    title: str | None = None
    company: str | None = None
    company_id: str | None = None
    location: str | None = None
    description: str | None = None
    employment_type: str | None = None
    posted_at: str | None = None
    url: str | None = Field(None, alias="applyUrl")


class LinkedInPost(_Base):
    id: str | None = None
    text: str | None = None
    author: dict[str, Any] | None = None
    likes_count: int | None = None
    comments_count: int | None = None
    shares_count: int | None = None
    created_at: str | None = None


class LinkedInUser(_Base):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    headline: str | None = None
    summary: str | None = None
    profile_pic_url: str | None = None
    location: str | None = None
    follower_count: int | None = None
    connection_count: int | None = None


# ---------------------------------------------------------------------------
# TikTok
# ---------------------------------------------------------------------------


class TikTokVideo(_Base):
    id: str | None = None
    description: str | None = None
    created_at: str | None = None
    author: dict[str, Any] | None = None
    stats: dict[str, Any] | None = None
    music: dict[str, Any] | None = None
    video_url: str | None = None
    cover_url: str | None = None
    duration: int | None = None


class TikTokUser(_Base):
    id: str | None = None
    username: str | None = None
    nickname: str | None = Field(None, alias="displayName")
    avatar: str | None = Field(None, alias="avatarUrl")
    bio: str | None = None
    signature: str | None = None
    verified: bool = False
    follower_count: int | None = Field(None, alias="followers")
    following_count: int | None = Field(None, alias="following")
    heart_count: int | None = Field(None, alias="hearts")
    video_count: int | None = None


class TikTokComment(_Base):
    id: str | None = None
    text: str | None = None
    user: dict[str, Any] | None = None
    like_count: int | None = None
    reply_count: int | None = None
    created_at: str | None = None


class TikTokCategory(_Base):
    id: str | None = None
    name: str | None = None


# ---------------------------------------------------------------------------
# Job104
# ---------------------------------------------------------------------------


class Job104Job(_Base):
    id: str | None = Field(None, alias="jobId")
    title: str | None = Field(None, alias="jobName")
    company_id: str | None = None
    company_name: str | None = None
    location: str | None = Field(None, alias="area")
    description: str | None = None
    salary: str | None = None
    employment_type: str | None = None
    posted_at: str | None = Field(None, alias="appearedAt")
    url: str | None = Field(None, alias="link")
    tags: list[str] = []
    requirements: list[str] = []


class Job104Company(_Base):
    id: str | None = None
    name: str | None = None
    description: str | None = None
    industry: str | None = None
    employee_count: str | None = None
    website: str | None = None
    address: str | None = None
    logo_url: str | None = None


# ---------------------------------------------------------------------------
# Bulk Job
# ---------------------------------------------------------------------------


class BulkJobStatus(_Base):
    job_id: str
    status: str  # "queued", "processing", "completed", "failed"
    total: int | None = None
    completed: int | None = None
    failed: int | None = None
    created_at: str | None = None


class BulkJob(_Base):
    job_id: str
    status: str = "queued"


# ---------------------------------------------------------------------------
# YouTube
# ---------------------------------------------------------------------------


class YouTubeVideo(_Base):
    id: str | None = None
    title: str | None = None
    description: str | None = None
    channel_id: str | None = None
    channel_title: str | None = None
    view_count: int | None = None
    like_count: int | None = None
    comment_count: int | None = None
    duration: str | None = None
    published_at: str | None = None
    thumbnail: str | None = None
    keywords: list[str] = []


class YouTubeChannel(_Base):
    id: str | None = None
    title: str | None = None
    description: str | None = None
    subscriber_count: int | None = None
    video_count: int | None = None
    view_count: int | None = None
    thumbnail: str | None = None
    banner: str | None = None
    created_at: str | None = None
    country: str | None = None


class YouTubeComment(_Base):
    id: str | None = None
    text: str | None = None
    author: str | None = None
    author_channel_id: str | None = None
    author_avatar: str | None = None
    is_verified: bool = False
    like_count: int | None = None
    reply_count: int | None = None
    published_at: str | None = None


# ---------------------------------------------------------------------------
# Dcard
# ---------------------------------------------------------------------------


class DcardForum(_Base):
    alias: str | None = None
    name: str | None = None
    description: str | None = None
    is_school: bool = False
    post_count: dict[str, Any] | None = None
    subscription_count: int | None = None


class DcardPost(_Base):
    id: int | None = None
    title: str | None = None
    excerpt: str | None = None
    content: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    forum_alias: str | None = None
    forum_name: str | None = None
    comment_count: int | None = None
    like_count: int | None = None
    topics: list[str] = []
    media: list[dict[str, Any]] = []


class DcardPersona(_Base):
    username: str | None = None
    nickname: str | None = None
    post_count: int | None = None
    gender: str | None = None


# ---------------------------------------------------------------------------
# Google Maps
# ---------------------------------------------------------------------------


class GMapsPlace(_Base):
    name: str | None = None
    category: str | None = None
    address: str | None = None
    website: str | None = None
    phone: str | None = None
    rating: float | None = None
    description: str | None = None
    hours: str | None = None
    lat: float | None = None
    lng: float | None = None
    place_id: str | None = None
    price_level: str | None = None
    photo_count: int | None = None
    url: str | None = None
