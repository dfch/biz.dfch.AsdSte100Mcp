# AGENTS.md

Quick reference for OpenCode agents working on **biz.dfch.AsdSte100Mcp** — an MCP server for ASD-STE100 Issue 9 standard.

## Project Shape

- **Type**: Python package + MCP server
- **Namespace**: `biz.dfch.asdste100mcp` (located in `src/biz/dfch/asdste100mcp/`)
- **Entry point**: `ste100-mcp` CLI command (defined in `pyproject.toml:93`)
- **License**: AGPL-3.0-or-later
- **Python**: 3.11, 3.12, 3.13 (multi-version testing required)
- **Package manager**: `uv` (not pip)

## Developer Commands

All commands use `uv run --frozen` to ensure reproducible environments.

### Run linters (ruff + pylint)
```bash
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py')
```

### Run all tests
```bash
uv run --frozen python -m unittest discover -v -s tests -t . -p "test_*.py"
```

### Install dev dependencies
```bash
uv sync --all-extras
```

### Run the MCP server locally (stdio mode)
```bash
uv run --frozen ste100-mcp
```

### Run the MCP server with extra vocabulary files
```bash
uv run --frozen ste100-mcp --file /path/to/custom.jsonl --file /path/to/extra.jsonl
```

### Run the MCP server in SSE/network mode (development only)
```bash
uv run --frozen ste100-mcp --transport sse --host 127.0.0.1 --port 8000
```

## Key Architecture

### MCP Server Structure
- **Server module**: `src/biz/dfch/asdste100mcp/server.py` — MCPServer instance, tool registration
- **CLI entry**: `src/biz/dfch/asdste100mcp/cli.py` — Typer CLI with dual-transport support (stdio/SSE)
- **Tools**: Each in `src/biz/dfch/asdste100mcp/tools/` — read-only search tools,
  grouped into two sub-packages
  - `words/` — vocabulary tools (`word_*`)
    - `find.py` — exact term lookup
    - `match.py` — regex pattern search
    - `similar.py` — fuzzy matching
    - `list.py` — all entries (expensive)
    - `count.py` — entry count only
  - `rules/` — ruleset tools (`rules_*`)
    - `find.py` — exact id lookup
    - `match.py` — regex over name/summary
    - `search.py` — full-text search across all content
    - `by_section.py` / `by_category.py` — exact section/category lookup
    - `examples.py` — content items, optionally scoped/filtered
    - `overview.py` — lightweight per-rule overview
    - `toc.py` — (section, category) table-of-contents outline

### Data Models
- `models/word.py` — Word model
- `models/word_meaning.py` — WordMeaning
- `models/word_note.py` — WordNote

### Configuration
- `settings.py` — Pydantic `Settings` model + `Factory` singleton:
  - `STE100_MCP_TRANSPORT` (stdio/sse)
  - `STE100_MCP_HOST`, `STE100_MCP_PORT` (SSE only)
  - `STE100_MCP_FILES` — colon-separated custom vocabulary paths
  - `STE100_MCP_USE_STE100` (load built-in vocab)
  - `STE100_MCP_USE_STE100_TECHNICAL_WORDS` (load technical words)
- `Factory.create_instance(extra_files)` — called once by the CLI before
  `mcp.run()`; merges CLI `--file` paths with `STE100_MCP_FILES`.
- `Factory.get_instance()` — called by `_lifespan` in `server.py`;
  asserts `create_instance` was called first.

## Testing

- **Framework**: Standard Python `unittest` (not pytest)
- **Test layout**: `tests/` mirrors `src/` structure (`tests/models/`, `tests/settings/`, `tests/tools/`)
- **Discovery**: `python -m unittest discover` (required pattern: `test_*.py`)
- **CI**: `.github/workflows/ci.yml` runs tests on Python 3.11, 3.12, 3.13

## CI/Release Workflow

- **Branch strategy**: `dev` (feature branch) → `main` (stable) → tag → publish
- **CI trigger**: Pylint + ruff checks + unittest on push/PR (all Python versions)
- **Release**: Tag on `main` triggers `publish.yml` → TestPyPI → PyPI
- **Publishing**: OIDC Trusted Publishing (no secrets in repo)

## Code Style

- **Formatter**: ruff (not black)
- **Line length**: 120 characters (`pyproject.toml:96`)
- **Linter**: pylint (as fallback; ruff is primary)
- **Lint rules**: E, F, W from ruff; tests ignore E501 (line length)

## Dependencies

- **Runtime**: `mcp`, `typer`, `pydantic-settings`, `biz-dfch-ste100vocab` (vocabulary data)
- **Dev**: ruff, pylint, mcp[cli], build, twine, pyinstaller, coverage
- **.env support**: `python-dotenv` with auto-discovery (walks upward from entry point)

## Important Gotchas

- **uv not pip**: Always use `uv` commands; `pip` is not the project standard
- **--frozen flag**: Lock file (`uv.lock`) is tracked; use `--frozen` to enforce reproducibility
- **Multi-version testing**: Agents must run tests on 3.11, 3.12, 3.13 before approval
- **Vocab is external**: Actual vocabulary data lives in `biz-dfch-ste100vocab` package (not in this repo)
- **Lifespan pattern**: MCP server loads vocab once at startup via lifespan context manager (`server.py`)
- **Read-only tools**: All five tools are read-only; no state modification
- **.env auto-loading**: CLI pre-loads `.env` before Typer parses args (`cli.py`)

## Package Publishing

- **Package name**: `biz-dfch-asdste100mcp` (PyPI, distinct from repo name)
- **Version**: Single source in `pyproject.toml:7`
- **Build system**: `setuptools` with `src/` layout
- **Data files**: Includes `*.jsonl` from `biz/dfch/asdste100mcp/data/` + `py.typed` marker

## Entry Points

- **CLI command**: `ste100-mcp` (typer CLI app defined in `cli.py`)
- **Module entry**: `python -m biz.dfch.asdste100mcp` (runs `__main__.py`, which invokes `cli.app()`)
