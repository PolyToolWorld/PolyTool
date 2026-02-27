"""
PolyTool Bot CLI
================
Command-line interface using Click.
"""

import asyncio
import logging
import sys

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from . import __version__
from .config import get_settings

console = Console()


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )


@click.group()
@click.version_option(__version__, prog_name="polytool-bot")
def cli():
    """PolyTool - Polymarket Copy-Trading Bot"""
    pass


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
def run(verbose: bool):
    """Start the copy-trading bot."""
    setup_logging(verbose)

    settings = get_settings()

    # Validate required config
    if not settings.polytool_api_key:
        console.print("[red]Error:[/] POLYTOOL_API_KEY is not set")
        console.print("Get your API key at https://polytool.world/settings")
        sys.exit(1)

    if not settings.private_key:
        console.print("[red]Error:[/] PRIVATE_KEY is not set")
        sys.exit(1)

    if not settings.clob_api_key:
        console.print("[red]Error:[/] CLOB API credentials are not set")
        console.print("Connect your wallet at https://polytool.world to derive credentials")
        sys.exit(1)

    console.print(
        Panel(
            f"[bold green]PolyTool Bot v{__version__}[/]\n"
            f"API: {settings.api_url}\n"
            f"Poll interval: {settings.poll_interval}s",
            title="Starting",
        )
    )

    from .worker import Worker

    worker = Worker(settings)

    async def _run():
        try:
            await worker.run()
        except KeyboardInterrupt:
            pass
        finally:
            await worker.stop()

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped[/]")


@cli.command()
def status():
    """Check connection to PolyTool API and show tracked wallets."""
    settings = get_settings()

    if not settings.polytool_api_key:
        console.print("[red]Error:[/] POLYTOOL_API_KEY is not set")
        sys.exit(1)

    from .api.polytool import PolyToolAPI

    api = PolyToolAPI(settings)

    async def _status():
        # Check connection
        ok, msg = await api.check_connection()
        if ok:
            console.print(f"[green]Connected[/] {msg}")
        else:
            console.print(f"[red]Failed[/] {msg}")
            await api.close()
            return

        # Get config
        try:
            config = await api.get_config()
        except Exception as e:
            console.print(f"[red]Failed to get config:[/] {e}")
            await api.close()
            return

        console.print(f"Wallet: [cyan]{config.get('wallet_address', '?')}[/]")
        console.print(f"Proxy: [cyan]{config.get('proxy_wallet') or '—'}[/]")
        console.print(
            f"Credentials: {'[green]Yes[/]' if config.get('has_credentials') else '[red]No[/]'}"
        )

        wallets = config.get("tracked_wallets", [])
        if not wallets:
            console.print("\n[yellow]No tracked wallets configured[/]")
            console.print("Add wallets at https://polytool.world/copytrade")
        else:
            table = Table(title=f"Tracked Wallets ({len(wallets)})")
            table.add_column("Wallet", style="cyan")
            table.add_column("Label")
            table.add_column("Mode")
            table.add_column("Enabled")
            table.add_column("Size")

            for w in wallets:
                addr = w["wallet_address"]
                table.add_row(
                    f"{addr[:6]}...{addr[-4:]}",
                    w.get("label") or "—",
                    w.get("mode", "manual"),
                    "[green]Yes[/]" if w.get("is_enabled") else "[red]No[/]",
                    f"${w.get('fixed_amount', 5.0):.0f}" if w.get("size_mode") == "fixed"
                    else f"{w.get('proportional_multiplier', 1.0)}x",
                )

            console.print(table)

        await api.close()

    asyncio.run(_status())


@cli.command()
def configure():
    """Interactive configuration setup."""
    from pathlib import Path

    console.print(
        Panel(
            "[bold]PolyTool Bot Configuration[/]\n\n"
            "This will create a .env file with your settings.",
            title="Setup",
        )
    )

    env_path = Path(".env")
    if env_path.exists():
        if not click.confirm(".env file already exists. Overwrite?"):
            console.print("[yellow]Cancelled[/]")
            return

    api_key = click.prompt("PolyTool API Key", default="")
    private_key = click.prompt("Wallet Private Key", default="", hide_input=True)
    clob_key = click.prompt("CLOB API Key", default="")
    clob_secret = click.prompt("CLOB API Secret", default="", hide_input=True)
    clob_pass = click.prompt("CLOB API Passphrase", default="", hide_input=True)
    proxy = click.prompt("Proxy Wallet (optional)", default="")
    api_url = click.prompt("API URL", default="https://polytool.world")
    interval = click.prompt("Poll interval (seconds)", default=15, type=int)

    lines = [
        f"POLYTOOL_API_KEY={api_key}",
        f"PRIVATE_KEY={private_key}",
        f"CLOB_API_KEY={clob_key}",
        f"CLOB_API_SECRET={clob_secret}",
        f"CLOB_API_PASSPHRASE={clob_pass}",
        f"PROXY_WALLET={proxy}",
        f"API_URL={api_url}",
        f"POLL_INTERVAL={interval}",
    ]

    env_path.write_text("\n".join(lines) + "\n")
    console.print(f"\n[green]Configuration saved to {env_path}[/]")


if __name__ == "__main__":
    cli()
