"""Main CLI module for tpy-cli."""

import os
import click
from typing import Optional, Any
from pathlib import Path

from . import __version__
from .utils import load_environment, ensure_config
from .options import common_options, env_file_option

# Import commands here to avoid circular imports
# Commands are registered using the @main.command() decorator

@click.group()
@click.version_option(version=__version__)
@env_file_option()
@click.option(
    "--debug", is_flag=True, help="Enable debug output"
)
@click.pass_context
def main(ctx: click.Context, env_file: Optional[Path] = None, debug: bool = False, **kwargs: Any) -> None:
    """Trilium-py CLI - Command line interface for trilium-py.
    
    Configuration is loaded in this order:
      1. Command line arguments
      2. Environment variables
      3. Local .env file
      4. Global ~/.trilium-py/.env file
    """
    # Store debug flag in context
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    
    # Load environment from specified file if provided
    if env_file:
        if debug:
            click.echo(f"[DEBUG] Loading environment from {env_file}", err=True)
        load_environment(env_file)
    
    # Initialize context object with server and token
    try:
        ctx.obj["server"], ctx.obj["token"] = ensure_config(debug=debug)
    except click.UsageError as e:
        if debug:
            click.echo(f"[DEBUG] Configuration error: {e}", err=True)
        raise

# Import and register commands after main is defined
# This avoids circular imports
from .commands import notes, config  # noqa: E402

# Register command groups
main.add_command(notes.notes)
main.add_command(config.config)

if __name__ == "__main__":
    main()
