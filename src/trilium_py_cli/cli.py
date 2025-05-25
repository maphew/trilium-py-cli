"""Main CLI module for tpy-cli."""

import os
import click
from typing import Optional

from .commands import notes, config

# Common options
server_option = click.option(
    "--server",
    envvar="TRILIUM_SERVER",
    help="Trilium server URL (e.g., http://localhost:8080)",
    required=True,
)

token_option = click.option(
    "--token",
    envvar="TRILIUM_TOKEN",
    help="Trilium ETAPI token",
    required=True,
)

@click.group()
@click.version_option()
def main():
    """Trilium-py CLI - Command line interface for trilium-py."""
    pass

# Add command groups
main.add_command(notes.notes)
main.add_command(config.config)

if __name__ == "__main__":
    main()
