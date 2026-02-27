"""
Polymarket API Client
=====================
Read-only wrapper for Gamma, Data, and CLOB APIs.
Adapted from PolyTool backend polymarket_client.py.
"""

import logging
import httpx
from ..config import Settings

logger = logging.getLogger("polytool.polymarket")


class PolymarketAPI:
    def __init__(self, settings: Settings):
        self.gamma_url = settings.gamma_api_url
        self.data_url = settings.data_api_url
        self.clob_url = settings.clob_api_url
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0, connect=10.0),
                limits=httpx.Limits(max_connections=50, max_keepalive_connections=10),
            )
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    # --- Data API ---

    async def get_trades(self, address: str, limit: int = 50) -> list[dict]:
        client = self._get_client()
        resp = await client.get(
            f"{self.data_url}/trades",
            params={"user": address.lower(), "limit": limit},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_positions(self, address: str, limit: int = 100) -> list[dict]:
        client = self._get_client()
        resp = await client.get(
            f"{self.data_url}/positions",
            params={"user": address.lower(), "limit": limit, "sizeThreshold": 0},
        )
        resp.raise_for_status()
        return resp.json()

    # --- CLOB API ---

    async def get_orderbook(self, token_id: str) -> dict:
        client = self._get_client()
        resp = await client.get(
            f"{self.clob_url}/book",
            params={"token_id": token_id},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_midpoint(self, token_id: str) -> float:
        client = self._get_client()
        resp = await client.get(
            f"{self.clob_url}/midpoint",
            params={"token_id": token_id},
        )
        resp.raise_for_status()
        data = resp.json()
        return float(data.get("mid", 0))

    # --- Gamma API ---

    async def get_events(self, limit: int = 50) -> list[dict]:
        client = self._get_client()
        resp = await client.get(
            f"{self.gamma_url}/events",
            params={"closed": "false", "limit": limit, "order": "volume24hr"},
        )
        resp.raise_for_status()
        return resp.json()

    async def search_markets(self, query: str) -> list[dict]:
        client = self._get_client()
        resp = await client.get(
            f"{self.gamma_url}/search",
            params={"q": query},
        )
        resp.raise_for_status()
        return resp.json()
