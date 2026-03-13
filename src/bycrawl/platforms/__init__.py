"""ByCrawl platform namespaces."""

from .dcard import AsyncDcard, Dcard
from .facebook import AsyncFacebook, Facebook
from .gmaps import AsyncGMaps, GMaps
from .instagram import AsyncInstagram, Instagram
from .job104 import AsyncJob104, Job104
from .linkedin import AsyncLinkedIn, LinkedIn
from .reddit import AsyncReddit, Reddit
from .threads import AsyncThreads, Threads
from .tiktok import AsyncTikTok, TikTok
from .x import AsyncX, X
from .youtube import AsyncYouTube, YouTube

__all__ = [
    "Threads", "AsyncThreads",
    "Facebook", "AsyncFacebook",
    "X", "AsyncX",
    "Instagram", "AsyncInstagram",
    "Reddit", "AsyncReddit",
    "LinkedIn", "AsyncLinkedIn",
    "TikTok", "AsyncTikTok",
    "YouTube", "AsyncYouTube",
    "Dcard", "AsyncDcard",
    "GMaps", "AsyncGMaps",
    "Job104", "AsyncJob104",
]
