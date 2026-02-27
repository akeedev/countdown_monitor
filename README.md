# akepylib

A collection of notebooks and utility libraries for macOS automation and financial data analysis.
Development usually starts in a notebook, then moves into a library. Libraries may later be
extracted into standalone projects (see `spec/000-overview.md`).

## Requirements

- Python >= 3.12

## Installation

```bash
uv pip install -e .
```

## Development

```bash
uv run pytest
uv run mypy src/
uv run ruff check src/ tests/
```

## License

MIT — see [LICENSE](LICENSE).
