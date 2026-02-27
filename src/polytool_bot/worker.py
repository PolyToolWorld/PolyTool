"""
Copy-Trade Worker
=================
Main polling loop. Fetches config from PolyTool API,
monitors tracked wallets, and executes copy trades.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

from .config import Settings
from .state import State
from .api.polytool import PolyToolAPI
from .api.polymarket import PolymarketAPI
from .engine.copytrade import CopyTradeEngine
from .engine.executor import TradeExecutor

logger = logging.getLogger("polytool.worker")


class Worker:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.state = State(Path(settings.state_file))
        self.pt_api = PolyToolAPI(settings)
        self.polymarket = PolymarketAPI(settings)
        self.engine = CopyTradeEngine(self.polymarket)
        self.executor = TradeExecutor(settings)
        self._running = False

    async def run(self):
        """Main polling loop."""
        self._running = True
        logger.info(
            f"Worker started (poll interval: {self.settings.poll_interval}s)"
        )

        # Initial heartbeat
        try:
            hb = await self.pt_api.heartbeat()
            self.state.set_last_heartbeat(hb.get("server_time", ""))
            logger.info(f"Connected to PolyTool API as {hb.get('user', '?')}")
        except Exception as e:
            logger.error(f"Initial heartbeat failed: {e}")

        while self._running:
            try:
                await self._poll()
            except Exception as e:
                logger.error(f"Poll error: {e}", exc_info=True)

            await asyncio.sleep(self.settings.poll_interval)

    async def stop(self):
        self._running = False
        await self.pt_api.close()
        await self.polymarket.close()
        logger.info("Worker stopped")

    async def _poll(self):
        """Single poll cycle: fetch config, check wallets, execute trades."""
        # Get config from API
        config = await self.pt_api.get_config()
        tracked_wallets = config.get("tracked_wallets", [])

        if not tracked_wallets:
            return

        # Send heartbeat every cycle
        try:
            hb = await self.pt_api.heartbeat()
            self.state.set_last_heartbeat(hb.get("server_time", ""))
        except Exception:
            pass

        for wallet_cfg in tracked_wallets:
            if not wallet_cfg.get("is_enabled", False):
                continue

            wallet_address = wallet_cfg["wallet_address"]

            try:
                since = datetime.utcnow() - timedelta(minutes=5)
                new_trades = await self.engine.check_wallet_trades(
                    wallet_address, since=since
                )

                if not new_trades:
                    continue

                logger.info(
                    f"Found {len(new_trades)} new trades from "
                    f"{wallet_cfg.get('label') or wallet_address[:10]}..."
                )

                for trade in new_trades:
                    trade_id = trade.get("id") or trade.get("transactionHash", "")

                    # Skip if already seen (across restarts)
                    if self.state.is_trade_seen(wallet_address, trade_id):
                        continue

                    should_copy, reason = self.engine.should_copy_trade(trade, wallet_cfg)
                    context = await self.engine.get_trade_context(trade)

                    if should_copy and wallet_cfg.get("mode") == "auto":
                        copy_size = self.engine.calculate_copy_size(trade, wallet_cfg)

                        # Execute the copy trade
                        result = await self.executor.place_limit_order(
                            token_id=context["token_id"],
                            side=context["side"],
                            price=context["price"],
                            size=copy_size,
                            market_title=context.get("market_title", ""),
                        )

                        # Report to API
                        await self.pt_api.report_trade({
                            "action": f"COPY_{context['side']}",
                            "market_title": context.get("market_title", ""),
                            "token_id": context.get("token_id", ""),
                            "outcome": context.get("outcome", ""),
                            "side": context["side"],
                            "price": context["price"],
                            "size": copy_size,
                            "total_cost": context["price"] * copy_size,
                            "order_id": result.get("order_id", ""),
                            "status": result.get("status", "failed"),
                            "copied_from_wallet": wallet_address,
                            "error_message": result.get("error", ""),
                        })

                        logger.info(
                            f"Copy trade {'placed' if result['success'] else 'failed'}: "
                            f"{context['side']} {copy_size} @ ${context['price']:.4f}"
                        )
                    elif not should_copy:
                        # Report detection only
                        await self.pt_api.report_trade({
                            "action": f"DETECTED_{context['side']}",
                            "market_title": context.get("market_title", ""),
                            "token_id": context.get("token_id", ""),
                            "outcome": context.get("outcome", ""),
                            "side": context["side"],
                            "price": context["price"],
                            "size": context["size"],
                            "total_cost": context["price"] * context["size"],
                            "status": f"skipped: {reason}",
                            "copied_from_wallet": wallet_address,
                        })

                    self.state.mark_trade_seen(wallet_address, trade_id)

            except Exception as e:
                logger.error(
                    f"Error processing wallet {wallet_address[:10]}: {e}",
                    exc_info=True,
                )
