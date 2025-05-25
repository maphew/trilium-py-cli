"""Note-related commands for tpy-cli."""

import click
from typing import Optional, Any
from trilium_py.client import ETAPI

from ..options import common_options
from ..utils import ensure_config

@click.group()
def notes() -> None:
    """Manage Trilium notes."""
    pass

def get_etapi(ctx: click.Context) -> ETAPI:
    """Get ETAPI client from context or environment.
    
    Args:
        ctx: Click context object
        
    Returns:
        ETAPI: Initialized ETAPI client
        
    Raises:
        click.UsageError: If configuration is missing
    """
    debug = ctx.obj.get("debug", False)
    server = ctx.obj.get("server")
    token = ctx.obj.get("token")
    
    if debug:
        click.echo(f"[DEBUG] Creating ETAPI client with server: {server[:10]}...", err=True)
    
    try:
        return ETAPI(server, token)
    except Exception as e:
        if debug:
            click.echo(f"[DEBUG] Failed to create ETAPI client: {e}", err=True)
        raise click.UsageError(
            "Failed to connect to Trilium. Please check your server URL and token."
        )

@notes.command()
@click.argument("query")
@common_options
@click.pass_context
def search(ctx: click.Context, query: str, **kwargs: Any) -> None:
    """Search for notes matching QUERY."""
    try:
        ea = get_etapi(ctx)
        results = ea.search_note(query)
        for note in results:
            click.echo(f"{note['noteId']} - {note['title']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

@notes.command()
@click.argument("title")
@click.option("--parent-id", default="root", help="Parent note ID")
@click.option("--type", "note_type", default="text", help="Note type (text, code, etc.)")
@click.option("--mime", default="text/html", help="MIME type")
@click.option("--content", "", help="Note content")
@common_options
@click.pass_context
def create(
    ctx: click.Context,
    title: str,
    parent_id: str,
    note_type: str,
    mime: str,
    content: str,
    **kwargs: Any
) -> None:
    """Create a new note."""
    try:
        ea = get_etapi(ctx)
        note = ea.create_note(
            parentNoteId=parent_id,
            title=title,
            type=note_type,
            mime=mime,
            content=content or ""
        )
        click.echo(f"Created note: {note['noteId']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

# Add more note commands here as needed
