"""
Bot Configuration
=================
Pydantic-settings based configuration loaded from .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PolyTool API
    polytool_api_key: str = ""
    api_url: str = "https://polytool.world"

    # Polymarket CLOB credentials (auto-derived when you connect wallet at polytool.world)
    clob_api_key: str = ""
    clob_api_secret: str = ""
    clob_api_passphrase: str = ""

    # Wallet
    private_key: str = ""
    proxy_wallet: str = ""

    # Polymarket Builder attribution (optional, from builders.polymarket.com)
    poly_builder_api_key: str = ""
    poly_builder_secret: str = ""
    poly_builder_passphrase: str = ""

    # Polymarket endpoints
    clob_api_url: str = "https://clob.polymarket.com"
    gamma_api_url: str = "https://gamma-api.polymarket.com"
    data_api_url: str = "https://data-api.polymarket.com"
    chain_id: int = 137

    # Bot behaviour
    poll_interval: int = 15  # seconds between wallet checks
    state_file: str = "state.json"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    return Settings()
