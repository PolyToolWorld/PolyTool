"""
PolyTool API Client
===================
Communicates with the hosted PolyTool API via X-API-Key header.
"""

import logging
import httpx
from ..config import Settings

logger = logging.getLogger("polytool.api")


class PolyToolAPI:
    def __init__(self, settings: Settings):
        self.base_url = settings.api_url.rstrip("/")
        self.api_key = settings.polytool_api_key
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={"X-API-Key": self.api_key},
                timeout=httpx.Timeout(30.0, connect=10.0),
            )
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def get_config(self) -> dict:
        """Get tracked wallets and copytrade configs."""
        client = self._get_client()
        resp = await client.get("/api/bot/config")
        resp.raise_for_status()
        return resp.json()

    async def report_trade(self, trade: dict) -> dict:
        """Report an executed trade to the server."""
        client = self._get_client()
        resp = await client.post("/api/bot/trade", json=trade)
        resp.raise_for_status()
        return resp.json()

    async def heartbeat(self) -> dict:
        """Send heartbeat to show bot is alive."""
        client = self._get_client()
        resp = await client.post("/api/bot/heartbeat")
        resp.raise_for_status()
        return resp.json()

    async def check_connection(self) -> tuple[bool, str]:
        """Check API connectivity. Returns (ok, message)."""
        try:
            data = await self.heartbeat()
            return True, f"Connected as {data.get('user', 'unknown')}"
        except httpx.HTTPStatusError as e:
            return False, f"API error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return False, f"Connection failed: {e}"
