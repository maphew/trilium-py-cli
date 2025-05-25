"""Configuration commands for tpy-cli."""

import os
import click
from pathlib import Path
from typing import Optional, Dict, Any

from ..utils import DEFAULT_CONFIG_DIR, GLOBAL_ENV_FILE, load_environment
from ..options import common_options, server_option, token_option

CONFIG_DIR = DEFAULT_CONFIG_DIR
CONFIG_FILE = CONFIG_DIR / ".env"

def create_env_file(server: Optional[str] = None, token: Optional[str] = None) -> Path:
    """Create or update .env file with configuration.
    
    Args:
        server: Optional server URL to set
        token: Optional token to set
        
    Returns:
        Path to the created/updated .env file
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read existing config if it exists
    config: Dict[str, str] = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key] = value.strip('"\'')
    
    # Update with new values
    if server is not None:
        config["TRILIUM_SERVER"] = server
    if token is not None:
        config["TRILIUM_TOKEN"] = token
    
    # Write back to file
    with open(CONFIG_FILE, 'w') as f:
        for key, value in config.items():
            f.write(f'{key}="{value}"\n')
    
    # Set permissions to be user-only
    CONFIG_FILE.chmod(0o600)
    return CONFIG_FILE

@click.group()
def config():
    """Manage tpy-cli configuration."""
    pass

@config.command()
@click.option("--server", help="Set default Trilium server URL")
@click.option("--token", help="Set default ETAPI token")
@click.option("--global", "use_global", is_flag=True, help="Use global config file instead of local")
def set(server: Optional[str] = None, token: Optional[str] = None, use_global: bool = False):
    """Set configuration values in .env file."""
    target_file = GLOBAL_ENV_FILE if use_global else CONFIG_FILE
    
    if not (server or token):
        click.echo("No configuration values provided. Use --server or --token options.")
        return
    
    env_file = create_env_file(server, token)
    click.echo(f"Configuration saved to {env_file}")

@config.command()
@click.option("--global", "use_global", is_flag=True, help="Show global config file instead of local")
@click.option("--all", "show_all", is_flag=True, help="Show all environment variables, not just Trilium ones")
def show(use_global: bool = False, show_all: bool = False):
    """Show current configuration."""
    target_file = GLOBAL_ENV_FILE if use_global else CONFIG_FILE
    
    if not target_file.exists():
        click.echo(f"No configuration file found at {target_file}")
        return
    
    click.echo(f"Configuration file: {target_file}")
    click.echo("-" * 40)
    
    with open(target_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            key, value = line.split('=', 1)
            value = value.strip('"\'')
            
            if show_all or key.startswith('TRILIUM_'):
                if key == 'TRILIUM_TOKEN' and len(value) > 8:
                    value = f"{value[:4]}...{value[-4:]}"
                click.echo(f"{key}={value}")

@config.command()
@click.option("--global", "use_global", is_flag=True, help="Use global config file instead of local")
@click.confirmation_option(prompt="Are you sure you want to clear the configuration?")
def clear(use_global: bool = False):
    """Clear configuration file."""
    target_file = GLOBAL_ENV_FILE if use_global else CONFIG_FILE
    
    if target_file.exists():
        target_file.unlink()
        click.echo(f"Configuration file {target_file} has been removed.")
    else:
        click.echo(f"No configuration file found at {target_file}")
