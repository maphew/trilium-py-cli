"""Commands for displaying Trilium server information."""

import click
from typing import Optional, Any
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from trilium_py.client import ETAPI

# Import utils here to avoid circular imports
from .. import utils

console = Console()

def display_app_info(app_info: dict, server_url: Optional[str] = None) -> None:
    """Display application information in a formatted panel.
    
    Args:
        app_info: Dictionary containing application information
        server_url: Optional server URL to display
    """
    # Create a mapping of field names to display names
    display_names = {
        'appName': 'Application',
        'app': 'Application',
        'appVersion': 'Version',
        'buildDate': 'Build Date',
        'buildRevision': 'Build Revision',
        'dbVersion': 'Database Version',
        'syncVersion': 'Sync Protocol Version',
        'dataDirectory': 'Data Directory'
        # Add more mappings as needed
    }
    
    # Convert all values to strings and create display properties
    properties = [("Server", server_url)]  # server_url is guaranteed to be present
    
    # Process all fields from app_info
    for key, value in app_info.items():
        if value is None:
            continue
            
        # Skip raw data or large binary fields
        if isinstance(value, (bytes, bytearray)):
            continue
            
        # Get display name or use the key with first letter capitalized
        display_name = display_names.get(key, key[0].upper() + key[1:])
        
        # Convert to string and handle common data types
        if isinstance(value, (list, dict)):
            # Skip complex objects for now
            continue
        elif isinstance(value, bool):
            display_value = "Yes" if value else "No"
        else:
            display_value = str(value)
            
        properties.append((display_name, display_value))
    
    # Sort properties by display name for consistent output
    properties.sort(key=lambda x: x[0])
    
    if not properties:
        console.print("[yellow]No server information available[/]")
        return
    
    # Find the longest property name for alignment
    max_prop_len = max(len(prop) for prop, _ in properties)
    
    # Build the content with aligned properties
    content = []
    for prop, value in properties:
        content.append(f"[cyan]{prop.ljust(max_prop_len)}[/]: {value}")
    
    # Display in a panel
    console.print(Panel.fit(
        "\n".join(content),
        title="Trilium Server Information",
        border_style="blue"
    ))

@click.group()
def info() -> None:
    """Display information about the Trilium server."""
    pass

@info.command()
@click.pass_context
def server(ctx: click.Context) -> None:
    """Display information about the connected Trilium server."""
    try:
        # Get ETAPI client using the utility function
        ea = utils.get_etapi(ctx)
        
        # Get and display app info
        console.print("Fetching server information...")
        app_info = ea.app_info()
        
        # Display connection info
        server_url = ctx.obj.get('server', 'Unknown')
        token = ctx.obj.get('token', '')
        
        console.print(Panel.fit(
            f"[bold]Server:[/bold] {server_url}\n"
            f"[bold]Token:[/bold] {'*' * 8}...{token[-4:] if token else ''}",
            title="Connection Information",
            border_style="blue"
        ))
        
        # Display app info (pass server URL to be included in the main panel)
        display_app_info(app_info, server_url=server_url)
        
    except Exception as e:
        console.print(Panel.fit(
            f"[bold red]✗ Failed to connect: {str(e)}[/bold red]\n\n"
            "Please check your configuration and ensure:\n"
            "- Server URL is correct\n"
            "- Token is valid\n"
            "- Trilium server is running and accessible",
            title="Connection Failed",
            border_style="red"
        ))
        raise click.Abort()
