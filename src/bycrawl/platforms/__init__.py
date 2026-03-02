"""ByCrawl platform namespaces."""

from .facebook import AsyncFacebook, Facebook
from .instagram import AsyncInstagram, Instagram
from .job104 import AsyncJob104, Job104
from .linkedin import AsyncLinkedIn, LinkedIn
from .reddit import AsyncReddit, Reddit
from .threads import AsyncThreads, Threads
from .tiktok import AsyncTikTok, TikTok
from .x import AsyncX, X
from .xiaohongshu import AsyncXiaohongshu, Xiaohongshu

__all__ = [
    "Threads", "AsyncThreads",
    "Facebook", "AsyncFacebook",
    "X", "AsyncX",
    "Instagram", "AsyncInstagram",
    "Reddit", "AsyncReddit",
    "LinkedIn", "AsyncLinkedIn",
    "Xiaohongshu", "AsyncXiaohongshu",
    "TikTok", "AsyncTikTok",
    "Job104", "AsyncJob104",
]
