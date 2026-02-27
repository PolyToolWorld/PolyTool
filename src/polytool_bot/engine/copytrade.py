"""
Copy-Trade Engine
=================
Core copy-trading logic. Adapted from PolyTool backend.
Works with dict configs from HTTP API instead of ORM models.
"""

import logging
from datetime import datetime
from typing import Optional

from ..api.polymarket import PolymarketAPI

logger = logging.getLogger("polytool.copytrade")


class CopyTradeEngine:
    def __init__(self, polymarket: PolymarketAPI):
        self.polymarket = polymarket
        self._last_seen_trades: dict[str, str] = {}

    async def check_wallet_trades(
        self, wallet_address: str, since: Optional[datetime] = None
    ) -> list[dict]:
        """Fetch recent trades for a wallet and return only new ones."""
        try:
            trades = await self.polymarket.get_trades(wallet_address, limit=50)
            if not trades:
                return []

            # Filter by time
            if since:
                since_ts = since.timestamp()
                trades = [
                    t for t in trades
                    if _parse_trade_time(t) and _parse_trade_time(t) > since_ts
                ]

            # Filter already seen
            last_seen = self._last_seen_trades.get(wallet_address)
            new_trades = []
            for trade in trades:
                trade_id = trade.get("id") or trade.get("transactionHash", "")
                if trade_id == last_seen:
                    break
                new_trades.append(trade)

            # Update last seen
            if trades:
                first_id = trades[0].get("id") or trades[0].get("transactionHash", "")
                self._last_seen_trades[wallet_address] = first_id

            return new_trades

        except Exception as e:
            logger.error(f"Error checking wallet {wallet_address[:10]}...: {e}")
            return []

    def should_copy_trade(self, trade: dict, config: dict) -> tuple[bool, str]:
        """
        Decide whether to copy a trade based on config dict.

        Config keys: is_enabled, mode, min_trade_size, copy_sells, max_price, min_price
        """
        if not config.get("is_enabled", False):
            return False, "copy-trading disabled"

        trade_size = float(trade.get("size", 0) or trade.get("amount", 0) or 0)
        if trade_size < config.get("min_trade_size", 1.0):
            return False, f"trade too small ({trade_size})"

        side = trade.get("side", "").upper()
        if side == "SELL" and not config.get("copy_sells", True):
            return False, "sell copying disabled"

        price = float(trade.get("price", 0) or 0)
        if price > 0:
            if price > config.get("max_price", 0.95):
                return False, f"price too high ({price})"
            if price < config.get("min_price", 0.01):
                return False, f"price too low ({price})"

        if config.get("mode") == "manual":
            return False, "manual mode - notification only"

        return True, "ok"

    def calculate_copy_size(self, trade: dict, config: dict) -> float:
        """Calculate copy size based on strategy config dict."""
        original_size = float(trade.get("size", 0) or trade.get("amount", 0) or 0)
        size_mode = config.get("size_mode", "fixed")

        if size_mode == "fixed":
            return config.get("fixed_amount", 5.0)
        elif size_mode == "proportional":
            return original_size * config.get("proportional_multiplier", 1.0)
        elif size_mode == "percentage":
            return original_size * (config.get("proportional_multiplier", 1.0) / 100)

        return config.get("fixed_amount", 5.0)

    async def get_trade_context(self, trade: dict) -> dict:
        """Enrich trade with market info."""
        token_id = trade.get("asset", "") or trade.get("tokenId", "")
        context = {
            "token_id": token_id,
            "market_slug": trade.get("market", "") or trade.get("marketSlug", ""),
            "market_title": trade.get("title", ""),
            "outcome": trade.get("outcome", ""),
            "side": trade.get("side", "BUY"),
            "price": float(trade.get("price", 0) or 0),
            "size": float(trade.get("size", 0) or trade.get("amount", 0) or 0),
        }

        if token_id:
            try:
                orderbook = await self.polymarket.get_orderbook(token_id)
                bids = orderbook.get("bids", [])
                asks = orderbook.get("asks", [])
                context["best_bid"] = float(bids[0]["price"]) if bids else 0
                context["best_ask"] = float(asks[0]["price"]) if asks else 0
                context["spread"] = context["best_ask"] - context["best_bid"]
            except Exception:
                pass

        return context


def _parse_trade_time(trade: dict) -> Optional[float]:
    ts = trade.get("timestamp") or trade.get("createdAt") or trade.get("matchTime")
    if not ts:
        return None
    try:
        if isinstance(ts, (int, float)):
            return float(ts)
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.timestamp()
    except Exception:
        return None
