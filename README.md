# tpy-cli

Trilium-py CLI - Command line interface for [trilium-py][trilium-py], providing easy access to Trilium Notes from your terminal.

Status: **alpha**, subject to exploring the wilds change. Hmmm, what would _this_ do? ...oh. Did I back up? I did, right?

## Installation

```bash
uv tool install git+https://github.com/maphew/trilium-py-cli
```

This will make the `tpy` command available in your shell. 

(On Windows or systems where git is not in PATH, download the repo archive, unpack it, and run `uv tool install .` from the root directory of the repo.)

## Usage

```
❯ tpy
Usage: tpy [OPTIONS] COMMAND [ARGS]...

  Trilium-py CLI - Command line interface for trilium-py.

Options:
  --version        Show the version and exit.
  --env-file FILE  Path to .env file to load
  --debug          Enable debug output
  --help           Show this message and exit.

Commands:
  config  Manage tpy-cli configuration.
  info    Display information about the Trilium server.
  notes   Manage Trilium notes.
```

Get and save token to .env file:

```
tpy config get-token
```

```
❯ tpy config get-token --server https://www.example.org
Enter your Trilium password: 
Connecting to Trilium server at https://www.example.org...
╭─────────────────── Server Information ───────────────────╮
│ Trilium: 0.93.0                                          │
│ Build Date: 2025-04-17T19:25:28Z                         │
│ Build Revision: 8211fd36af3149c60014737eee2407abb5516974 │
╰──────────────────────────────────────────────────────────╯
╭───── Authentication Token ─────╮
│ Server: https://www.example.org│
│ Token: Oo919mXP...TdI=         │
╰────────────────────────────────╯

✓ Token saved to: .env

✓ Successfully connected to Trilium v0.93.0
```

Show configured server info

```
❯ tpy info server
```

```
Fetching server information...
╭──────────────────── Trilium Server Information ────────────────────╮
│ Server                  : https://www.example.org                  │
│ Token                   : OYE=..............nLNz                   │
│ App Version             : 0.93.0                                   │
│ Db Version              : 229                                      │
│ Node Version            : v22.14.0                                 │
│ Sync Version            : 34                                       │
│ Build Date              : 2025-04-17T19:25:28Z                     │
│ Build Revision          : 8211fd36af3149c60014737eee2407abb5516974 │
│ Data Directory          : /home/node/trilium-data                  │
│ Clipper Protocol Version: 1.0                                      │
│ Utc Date Time           : 2025-04-27T01:06:03.891Z                 │
╰────────────────────────────────────────────────────────────────────╯
```

-----

# Stubs, not well tested

### Search Notes

```bash
tpy notes search "your search query"
```

### Create a Note

```bash
tpy notes create "Note Title" --parent-id root --type text
```

### Show Help

```bash
tpy --help
tpy notes --help
tpy config --help
```

## Development

1. Clone the repository
2. Install with development dependencies:
   ```bash
   uv pip install -e .[dev]
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT


[trilium-py]: https://github.com/Nriver/trilium-py