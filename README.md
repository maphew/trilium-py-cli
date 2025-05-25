# tpy-cli

[![PyPI version](https://img.shields.io/pypi/v/tpy-cli.svg)](https://pypi.org/project/tpy-cli/)
[![License](https://img.shields.io/pypi/l/tpy-cli.svg)](https://github.com/maphew/tpy-cli/blob/main/LICENSE)

A command-line interface for [trilium-py](https://github.com/Nriver/trilium-py), providing easy access to Trilium Notes from your terminal.

## Installation

```bash
uv pip install tpy-cli
```

## Configuration

Set your default Trilium server and token:

```bash
tpy config set --server http://localhost:8080 --token YOUR_ETAPI_TOKEN
```

## Usage

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
