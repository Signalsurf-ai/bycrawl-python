"""Tests for ByCrawl / AsyncByCrawl client initialization."""

from __future__ import annotations

import pytest

from bycrawl import AsyncByCrawl, ByCrawl


class TestByCrawlInit:
    def test_requires_api_key(self):
        with pytest.raises(ValueError, match="api_key must be provided"):
            ByCrawl()

    def test_accepts_api_key_kwarg(self):
        client = ByCrawl(api_key="sk_byc_test")
        assert client._transport._api_key == "sk_byc_test"
        client.close()

    def test_reads_env_var(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("BYCRAWL_API_KEY", "sk_byc_env")
        client = ByCrawl()
        assert client._transport._api_key == "sk_byc_env"
        client.close()

    def test_explicit_key_overrides_env(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("BYCRAWL_API_KEY", "sk_byc_env")
        client = ByCrawl(api_key="sk_byc_explicit")
        assert client._transport._api_key == "sk_byc_explicit"
        client.close()

    def test_context_manager(self):
        with ByCrawl(api_key="sk_byc_test") as client:
            assert client.threads is not None

    def test_all_namespaces_exist(self):
        client = ByCrawl(api_key="sk_byc_test")
        for ns in [
            "threads", "facebook", "x", "instagram", "reddit",
            "linkedin", "tiktok", "youtube", "dcard", "gmaps",
            "job104", "web",
        ]:
            assert hasattr(client, ns), f"Missing namespace: {ns}"
        client.close()


class TestAsyncByCrawlInit:
    def test_requires_api_key(self):
        with pytest.raises(ValueError, match="api_key must be provided"):
            AsyncByCrawl()

    def test_accepts_api_key_kwarg(self):
        client = AsyncByCrawl(api_key="sk_byc_test")
        assert client._transport._api_key == "sk_byc_test"

    def test_all_namespaces_exist(self):
        client = AsyncByCrawl(api_key="sk_byc_test")
        for ns in [
            "threads", "facebook", "x", "instagram", "reddit",
            "linkedin", "tiktok", "youtube", "dcard", "gmaps",
            "job104", "web",
        ]:
            assert hasattr(client, ns), f"Missing namespace: {ns}"
