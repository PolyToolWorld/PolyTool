"""
Builder Signing
===============
HMAC signing for Polymarket builder order attribution.
Adapted from PolyTool backend builder_signer.py.
"""

import hmac
import hashlib
import time


def build_hmac_signature(
    secret: str, timestamp: int, method: str, path: str, body: str = ""
) -> str:
    message = f"{timestamp}{method}{path}{body}"
    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def get_builder_headers(
    api_key: str, secret: str, passphrase: str, method: str, path: str, body: str = ""
) -> dict:
    if not api_key:
        return {}

    timestamp = str(int(time.time() * 1000))
    signature = build_hmac_signature(secret, int(timestamp), method, path, body)

    return {
        "POLY_BUILDER_API_KEY": api_key,
        "POLY_BUILDER_TIMESTAMP": timestamp,
        "POLY_BUILDER_PASSPHRASE": passphrase,
        "POLY_BUILDER_SIGNATURE": signature,
    }
