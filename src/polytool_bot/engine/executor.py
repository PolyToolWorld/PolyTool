"""
Trade Executor
==============
Executes trades on Polymarket via CLOB API.
Adapted from PolyTool backend trade_executor.py.
"""

import logging
from ..config import Settings

logger = logging.getLogger("polytool.executor")


class TradeExecutor:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._client = None

    def _get_clob_client(self):
        if self._client is None:
            from py_clob_client.client import ClobClient, ApiCreds

            creds = ApiCreds(
                api_key=self.settings.clob_api_key,
                api_secret=self.settings.clob_api_secret,
                api_passphrase=self.settings.clob_api_passphrase,
            )
            sig_type = 2 if self.settings.proxy_wallet else 0
            self._client = ClobClient(
                host=self.settings.clob_api_url,
                chain_id=self.settings.chain_id,
                key=self.settings.private_key,
                creds=creds,
                signature_type=sig_type,
                funder=self.settings.proxy_wallet or None,
            )
        return self._client

    async def place_limit_order(
        self,
        token_id: str,
        side: str,
        price: float,
        size: float,
        market_title: str = "",
    ) -> dict:
        try:
            client = self._get_clob_client()
            from py_clob_client.clob_types import OrderArgs

            order_args = OrderArgs(
                price=price,
                size=size,
                side=side,
                token_id=token_id,
            )
            signed_order = client.create_order(order_args)
            result = client.post_order(signed_order)

            success = result.get("success", False) or result.get("orderID")
            logger.info(
                f"Order {'placed' if success else 'failed'}: "
                f"{side} {size}x @ ${price:.4f} | {market_title}"
            )
            return {
                "success": bool(success),
                "order_id": result.get("orderID", ""),
                "status": "placed" if success else "failed",
                "error": result.get("errorMsg", ""),
            }
        except Exception as e:
            logger.error(f"Order execution error: {e}")
            return {"success": False, "order_id": "", "status": "failed", "error": str(e)}

    async def place_market_order(
        self,
        token_id: str,
        side: str,
        amount: float,
        price: float,
    ) -> dict:
        try:
            client = self._get_clob_client()
            from py_clob_client.clob_types import MarketOrderArgs, OrderType

            order_args = MarketOrderArgs(
                token_id=token_id,
                amount=amount,
                price=price,
                side=side,
            )
            signed_order = client.create_market_order(order_args)
            result = client.post_order(signed_order, OrderType.FOK)

            success = result.get("success", False)
            return {
                "success": bool(success),
                "order_id": result.get("orderID", ""),
                "status": "filled" if success else "failed",
                "error": result.get("errorMsg", ""),
            }
        except Exception as e:
            logger.error(f"Market order error: {e}")
            return {"success": False, "error": str(e)}

    async def get_balance(self) -> float:
        try:
            client = self._get_clob_client()
            from py_clob_client.clob_types import BalanceAllowanceParams, AssetType

            result = client.get_balance_allowance(
                params=BalanceAllowanceParams(asset_type=AssetType.COLLATERAL)
            )
            return float(result.get("balance", 0)) / 1e6
        except Exception as e:
            logger.error(f"Balance check error: {e}")
            return 0.0
