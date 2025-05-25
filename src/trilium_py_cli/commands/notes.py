"""Note-related commands for tpy-cli."""

import click
from typing import Optional

@click.group()
def notes():
    """Manage Trilium notes."""
    pass

@notes.command()
@click.argument("query")
@click.option("--server", envvar="TRILIUM_SERVER", help="Trilium server URL")
@click.option("--token", envvar="TRILIUM_TOKEN", help="ETAPI token")
def search(query: str, server: str, token: str):
    """Search for notes matching QUERY."""
    from trilium_py.client import ETAPI
    
    try:
        ea = ETAPI(server, token)
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
@click.option("--server", envvar="TRILIUM_SERVER", help="Trilium server URL")
@click.option("--token", envvar="TRILIUM_TOKEN", help="ETAPI token")
def create(title: str, parent_id: str, note_type: str, mime: str, server: str, token: str):
    """Create a new note."""
    from trilium_py.client import ETAPI
    
    try:
        ea = ETAPI(server, token)
        note = ea.create_note(
            parentNoteId=parent_id,
            title=title,
            type=note_type,
            mime=mime,
            content=""
        )
        click.echo(f"Created note: {note['noteId']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

# Add more note commands here as needed
