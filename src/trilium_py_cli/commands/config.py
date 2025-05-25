"""Configuration commands for tpy-cli."""

import os
import click
from pathlib import Path
from typing import Optional, Dict, Any

from ..utils import ENV_FILE, load_environment
from ..options import common_options, server_option, token_option


def create_or_update_env(server: Optional[str] = None, token: Optional[str] = None) -> Path:
    """Create or update .env file with configuration.
    
    If .env file doesn't exist, it will be created in the current directory.
    If it exists, only the specified values will be updated.
    
    Args:
        server: Optional server URL to set
        token: Optional token to set
        
    Returns:
        Path to the created/updated .env file
    """
    # Read existing config if it exists
    config: Dict[str, str] = {}
    if ENV_FILE.exists():
        try:
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip('"\'\n')
        except Exception as e:
            click.echo(f"Warning: Could not read existing .env file: {e}", err=True)
    
    # Update with new values if provided
    if server is not None:
        config["TRILIUM_SERVER"] = server.strip()
    if token is not None:
        config["TRILIUM_TOKEN"] = token.strip()
    
    # Ensure we have at least server and token
    if not config.get("TRILIUM_SERVER") or not config.get("TRILIUM_TOKEN"):
        raise click.UsageError("Both server URL and token are required")
    
    # Create parent directories if they don't exist
    ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to file
    try:
        with open(ENV_FILE, 'w') as f:
            for key, value in config.items():
                if key and value:  # Skip empty keys or values
                    f.write(f"{key}={value}\n")
        
        # Set permissions to be user-only
        ENV_FILE.chmod(0o600)
        return ENV_FILE
    except Exception as e:
        raise click.UsageError(f"Failed to write to {ENV_FILE}: {e}")

@click.group()
def config():
    """Manage tpy-cli configuration.
    
    Configuration is stored in a .env file in the current directory.
    """
    pass


@config.command()
@server_option()
@token_option()
@click.pass_context
def set(ctx: click.Context, server: str, token: str) -> None:
    """Set configuration values in the local .env file."""
    try:
        env_file = create_or_update_env(server, token)
        click.echo(f"Configuration saved to {click.style(str(env_file), fg='green')}")
    except Exception as e:
        if ctx.obj.get('debug', False):
            raise
        click.echo(f"Error saving configuration: {e}", err=True)
        raise click.Abort()


@config.command()
@click.option(
    "--show-token", is_flag=True, 
    help="Show the full token (by default only shows first and last 4 characters)"
)
@click.pass_context
def show(ctx: click.Context, show_token: bool) -> None:
    """Show current configuration."""
    if not ENV_FILE.exists():
        click.echo("No .env file found in the current directory.")
        click.echo("\nTo create one, run:")
        click.echo("  tpy config set --server URL --token TOKEN")
        return
    
    click.echo(f"Configuration file: {click.style(str(ENV_FILE), fg='cyan')}")
    click.echo("-" * 60)
    
    try:
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    click.echo(click.style(line, fg='bright_black'))
                    continue
                    
                if '=' not in line:
                    continue
                    
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('\"\'')
                
                if key.startswith('TRILIUM_'):
                    if key == 'TRILIUM_TOKEN' and not show_token and len(value) > 8:
                        value = f"{value[:4]}...{value[-4:]}"
                    click.echo(f"{click.style(key, fg='green')}={click.style(value, fg='yellow')}")
    except Exception as e:
        if ctx.obj.get('debug', False):
            raise
        click.echo(f"Error reading configuration: {e}", err=True)
        raise click.Abort()
    
    if not show_token and ENV_FILE.exists() and any('TRILIUM_TOKEN' in line for line in open(ENV_FILE)):
        click.echo("\n" + click.style("Note: ", fg='yellow') + 
                  "Token is partially hidden. Use --show-token to display the full token.")


@config.command()
@click.confirmation_option(prompt="Are you sure you want to delete the .env file?")
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete the local .env file."""
    if not ENV_FILE.exists():
        click.echo("No .env file found in the current directory.")
        return
    
    try:
        ENV_FILE.unlink()
        click.echo(f"Deleted configuration file: {click.style(str(ENV_FILE), fg='red')}")
    except Exception as e:
        if ctx.obj.get('debug', False):
            raise
        click.echo(f"Error deleting configuration: {e}", err=True)
        raise click.Abort()
