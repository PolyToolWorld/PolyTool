"""
Local State Manager
===================
Tracks seen trades in a local JSON file to avoid duplicates across restarts.
"""

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("polytool.state")

STATE_FILE = Path("state.json")


class State:
    def __init__(self, path: Optional[Path] = None):
        self.path = path or STATE_FILE
        self._data: dict = {"seen_trades": {}, "last_heartbeat": None}
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                self._data = json.loads(self.path.read_text())
            except Exception as e:
                logger.warning(f"Failed to load state: {e}")

    def save(self):
        try:
            self.path.write_text(json.dumps(self._data, indent=2))
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def is_trade_seen(self, wallet: str, trade_id: str) -> bool:
        seen = self._data.get("seen_trades", {}).get(wallet, [])
        return trade_id in seen

    def mark_trade_seen(self, wallet: str, trade_id: str):
        if wallet not in self._data["seen_trades"]:
            self._data["seen_trades"][wallet] = []
        trades = self._data["seen_trades"][wallet]
        trades.append(trade_id)
        # Keep last 500 per wallet
        self._data["seen_trades"][wallet] = trades[-500:]
        self.save()

    def set_last_heartbeat(self, ts: str):
        self._data["last_heartbeat"] = ts
        self.save()
