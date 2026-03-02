# ByCrawl Python SDK

The official Python SDK for the [ByCrawl](https://bycrawl.com) social media data API.

Supports **Threads, Facebook, X (Twitter), Instagram, Reddit, LinkedIn, Xiaohongshu, TikTok, and 104**.

## Installation

```bash
pip install bycrawl
```

## Quick Start

```python
from bycrawl import ByCrawl

client = ByCrawl(api_key="sk_byc_...")

# Get a Threads post
post = client.threads.get_post("DQt-ox3kdE4")
print(post.data.text)
print(post.data.stats.likes)
```

## Platform Examples

### Threads

```python
# User profile
user = client.threads.get_user("zuck")
print(f"{user.data.username} — {user.data.follower_count} followers")

# Search posts
results = client.threads.search_posts("AI")
```

### X (Twitter)

```python
user = client.x.get_user("elonmusk")
tweet = client.x.get_post("1234567890")

# Auto-paginate all posts
for post in client.x.iter_user_posts("elonmusk"):
    print(post.text)
```

### Instagram

```python
user = client.instagram.get_user("instagram")
print(user.data.follower_count)
```

### TikTok

```python
video = client.tiktok.get_video("7123456789")
user = client.tiktok.get_user("khaby.lame")

# Browse trending
trending = client.tiktok.get_categories()
```

### Reddit

```python
sub = client.reddit.get_subreddit("python")
posts = client.reddit.get_subreddit_posts("python", sort="hot")
```

### LinkedIn

```python
company = client.linkedin.get_company("google")
jobs = client.linkedin.search_jobs("software engineer", location="Taiwan")

# Auto-paginate jobs
for job in client.linkedin.iter_search_jobs("data scientist"):
    print(job.title, job.location)
```

### Xiaohongshu

```python
notes = client.xiaohongshu.search_notes("咖啡推薦")
note = client.xiaohongshu.get_note("note_id")
```

### Facebook

```python
page = client.facebook.get_user("NASA")
posts = client.facebook.get_user_posts("NASA")
```

### 104 Jobs

```python
jobs = client.job104.search_jobs(q="Python工程師")
company = client.job104.get_company("company_id")
```

## Async Support

```python
import asyncio
from bycrawl import AsyncByCrawl

async def main():
    async with AsyncByCrawl(api_key="sk_byc_...") as client:
        post = await client.threads.get_post("DQt-ox3kdE4")
        print(post.data.text)

asyncio.run(main())
```

## Rate Limit & Credit Info

Every response includes rate limit and credit usage:

```python
resp = client.threads.get_post("DQt-ox3kdE4")
print(resp.rate_limit.remaining)  # requests left
print(resp.credit.remaining)      # credits left
```

## Error Handling

```python
from bycrawl import ByCrawl, NotFoundError, RateLimitError

try:
    client.threads.get_post("invalid")
except NotFoundError:
    print("Post not found")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
```

## Environment Variable

You can set your API key as an environment variable instead of passing it directly:

```bash
export BYCRAWL_API_KEY="sk_byc_..."
```

```python
client = ByCrawl()  # picks up from env
```

## Links

- [Website](https://bycrawl.com)
- [GitHub](https://github.com/Signalsurf-ai/bycrawl-python)
