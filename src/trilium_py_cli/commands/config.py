"""Configuration commands for tpy-cli."""

import os
import click
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".config" / "tpy"
CONFIG_FILE = CONFIG_DIR / "config.toml"

@click.group()
def config():
    """Manage tpy-cli configuration."""
    pass

@config.command()
@click.option("--server", help="Set default Trilium server URL")
@click.option("--token", help="Set default ETAPI token")
def set(server: Optional[str] = None, token: Optional[str] = None):
    """Set configuration values."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    config = {}
    if CONFIG_FILE.exists():
        config = eval(CONFIG_FILE.read_text())
    
    if server:
        config["server"] = server
    if token:
        config["token"] = token
    
    CONFIG_FILE.write_text(str(config))
    click.echo(f"Configuration saved to {CONFIG_FILE}")

@config.command()
def show():
    """Show current configuration."""
    if not CONFIG_FILE.exists():
        click.echo("No configuration file found.")
        return
    
    click.echo(f"Configuration file: {CONFIG_FILE}")
    click.echo(CONFIG_FILE.read_text())
