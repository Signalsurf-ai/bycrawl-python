"""Reddit platform namespace."""

from __future__ import annotations

from .._resource import APIResource, AsyncAPIResource
from .._types import APIResponse, RedditPost, RedditUser, Subreddit


class Reddit(APIResource):
    """Sync Reddit namespace."""

    def get_subreddit(self, name: str) -> APIResponse[Subreddit]:
        return self._get(f"/reddit/subreddits/{name}", cast_to=Subreddit)

    def get_subreddit_posts(
        self,
        name: str,
        *,
        sort: str | None = None,
        count: int | None = None,
    ) -> APIResponse[list[RedditPost]]:
        return self._get(
            f"/reddit/subreddits/{name}/posts",
            params={"sort": sort, "count": count},
            cast_to=RedditPost,
            items_key="posts",
        )

    def get_post(self, post_id: str) -> APIResponse[RedditPost]:
        return self._get(f"/reddit/posts/{post_id}", cast_to=RedditPost)

    def search_posts(
        self,
        q: str,
        *,
        sort: str | None = None,
        count: int | None = None,
    ) -> APIResponse[list[RedditPost]]:
        return self._get(
            "/reddit/posts/search",
            params={"q": q, "sort": sort, "count": count},
            cast_to=RedditPost,
            items_key="posts",
        )

    def get_user(self, username: str) -> APIResponse[RedditUser]:
        return self._get(f"/reddit/users/{username}", cast_to=RedditUser)


class AsyncReddit(AsyncAPIResource):
    """Async Reddit namespace."""

    async def get_subreddit(self, name: str) -> APIResponse[Subreddit]:
        return await self._get(f"/reddit/subreddits/{name}", cast_to=Subreddit)

    async def get_subreddit_posts(
        self,
        name: str,
        *,
        sort: str | None = None,
        count: int | None = None,
    ) -> APIResponse[list[RedditPost]]:
        return await self._get(
            f"/reddit/subreddits/{name}/posts",
            params={"sort": sort, "count": count},
            cast_to=RedditPost,
            items_key="posts",
        )

    async def get_post(self, post_id: str) -> APIResponse[RedditPost]:
        return await self._get(f"/reddit/posts/{post_id}", cast_to=RedditPost)

    async def search_posts(
        self,
        q: str,
        *,
        sort: str | None = None,
        count: int | None = None,
    ) -> APIResponse[list[RedditPost]]:
        return await self._get(
            "/reddit/posts/search",
            params={"q": q, "sort": sort, "count": count},
            cast_to=RedditPost,
            items_key="posts",
        )

    async def get_user(self, username: str) -> APIResponse[RedditUser]:
        return await self._get(f"/reddit/users/{username}", cast_to=RedditUser)
