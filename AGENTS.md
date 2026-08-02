# AGENTS.md

Quick reference for OpenCode agents working on **biz.dfch.AsdSte100Mcp** — an MCP server for ASD-STE100 Issue 9 standard.

## Project Shape

- **Type**: Python package + MCP server
- **Namespace**: `biz.dfch.asdste100mcp` (located in `src/biz/dfch/asdste100mcp/`)
- **Entry point**: `ste100-mcp` CLI command (defined in `pyproject.toml:96`)
- **License**: AGPL-3.0-or-later
- **Python**: `requires-python = ">=3.11"` (3.11–3.13 tested in CI); local dev
  defaults to 3.13 via `.python-version` — these are two separate settings,
  keep them in sync intentionally, not by accident
- **Package manager**: `uv` (not pip)

## Developer Commands

All commands use `uv run --frozen` to ensure reproducible environments.

### Run linters (ruff + pylint)
```bash
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py')
```
In CI, pylint runs with `|| true` — it never fails the build. Ruff is the
only enforced linter/formatter; treat pylint output as advisory.

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

### Run the MCP server with extra rules files
```bash
uv run --frozen ste100-mcp --rules-file /path/to/custom_rules.json
```

### Run the MCP server in SSE/network mode (development only)
```bash
uv run --frozen ste100-mcp --transport sse --host localhost --port 8000
```

## Key Architecture

### MCP Server Structure
- **Server module**: `src/biz/dfch/asdste100mcp/server.py` — MCPServer instance, tool registration
- **CLI entry**: `src/biz/dfch/asdste100mcp/cli.py` — Typer CLI with dual-transport support (stdio/SSE)
- **Tools**: Each in `src/biz/dfch/asdste100mcp/tools/` — read-only search tools,
  grouped into two sub-packages
  - `words/` — vocabulary tools (`word_*`)
    - `word_find.py` — exact term lookup
    - `word_match.py` — regex pattern search
    - `word_fuzzy.py` — fuzzy matching
    - `word_list.py` — all entries (expensive)
    - `word_count.py` — entry count only
  - `rules/` — ruleset tools (`rules_*`), backed by the external
    `biz-dfch-asdste100rules` library; return types reuse that library's
    own pydantic models (`Rule`, `ContentItem`, `RuleOverview`) directly
    instead of local wrappers
    - `rules_find.py` — exact id lookup
    - `rules_match.py` — regex over name/summary
    - `rules_search.py` — full-text search across all content
    - `rules_by_section.py` / `rules_by_category.py` — exact section/category lookup
    - `rules_examples.py` — content items, optionally scoped/filtered
    - `rules_overview.py` — lightweight per-rule overview
    - `rules_toc.py` — (section, category) table-of-contents outline
    - `_params.py` — shared `Annotated` parameter types for all rules tools

### Data Models
- `models/word.py` — Word model
- `models/word_meaning.py` — WordMeaning
- `models/word_note.py` — WordNote
- `models/toc_entry.py` — TocEntry (wraps the plain tuples `Rules.toc()` returns)

### Configuration
- `settings.py` — Pydantic `Settings` model + `Factory` singleton:
  - `STE100_MCP_TRANSPORT` (stdio/sse)
  - `STE100_MCP_HOST`, `STE100_MCP_PORT` (SSE only)
  - `STE100_MCP_FILES` — colon-separated custom vocabulary paths
  - `STE100_MCP_USE_STE100` (load built-in vocab)
  - `STE100_MCP_USE_STE100_TECHNICAL_WORDS` (load technical words)
  - `STE100_MCP_RULES_FILES` — colon-separated custom rules-file paths
  - `STE100_MCP_USE_STE100_RULES` (load built-in ruleset)
- `Factory.create_instance(extra_files, extra_rules_files)` — called once by
  the CLI before `mcp.run()`; merges CLI `--file`/`--rules-file` paths with
  `STE100_MCP_FILES`/`STE100_MCP_RULES_FILES`.
- `Factory.get_instance()` — called by `_lifespan` in `server.py`;
  asserts `create_instance` was called first.

**Gotcha**: `Factory` is a class-level singleton (`Factory._instance`), not
an instance. Tests that call `create_instance()` must reset it in
`tearDown()` via `Factory._instance = None`, or later tests will hit the
"already created" `AssertionError` — see `tests/settings/test_factory.py`.

## Testing

- **Framework**: Standard Python `unittest` (not pytest)
- **Test layout**: `tests/` mirrors `src/` structure (`tests/models/`, `tests/settings/`, `tests/tools/`)
  including the `tools/words/` and `tools/rules/` sub-packages
- **Discovery**: `python -m unittest discover` (required pattern: `test_*.py`)
- **CI**: `.github/workflows/ci.yml` runs tests on Python 3.11, 3.12, 3.13

## CI/Release Workflow

- **Branch strategy**: `dev` (feature branch) → `main` (stable) → tag → publish
- **CI trigger**: Pylint + ruff checks + unittest on push/PR (all Python versions)
- **Release**: Tag on `main` triggers `publish.yml` → TestPyPI → PyPI → GitHub Release
- **Publishing**: OIDC Trusted Publishing (no secrets in repo)
- **Version bumps**: update `version` in `pyproject.toml` (single source) and
  move the `[Unreleased]` section in `CHANGELOG.md` into a new dated
  `## [x.y.z] - YYYY-MM-DD` section (plus compare-link footnotes) in the
  same commit; see `README.md` § "Make a Release" for the full tag/publish steps

## Code Style

- **Formatter**: ruff (not black)
- **Line length**: 120 characters (`pyproject.toml:99`)
- **Linter**: pylint (as fallback; ruff is primary)
- **Lint rules**: E, F, W from ruff; tests ignore E501 (line length)

## Dependencies

- **Runtime**: `mcp`, `typer`, `pydantic-settings`, `biz-dfch-asdste100vocab`
  (vocabulary data), `biz-dfch-asdste100rules` (ruleset data)
- **Dev**: ruff, mcp[cli], build, twine, pyinstaller, coverage; `pylint` lives
  in the `test` extra, not `dev` — `dev` depends on `[test]`
- **.env support**: `python-dotenv` with auto-discovery (walks upward from entry point)

## Important Gotchas

- **uv not pip**: Always use `uv` commands; `pip` is not the project standard
- **--frozen flag**: Lock file (`uv.lock`) is tracked; use `--frozen` to enforce reproducibility
- **Multi-version testing**: Agents must run tests on 3.11, 3.12, 3.13 before approval
- **Vocab is external**: Actual vocabulary data lives in `biz-dfch-asdste100vocab` package (not in this repo)
- **Rules are external**: Ruleset data lives in `biz-dfch-asdste100rules` package (not in this repo)
- **Lifespan pattern**: MCP server loads vocab and rules once at startup via lifespan context manager (`server.py`)
- **Read-only tools**: All tools are read-only; no state modification
- **.env auto-loading**: CLI pre-loads `.env` before Typer parses args (`cli.py`)

## Package Publishing

- **Package name**: `biz-dfch-asdste100mcp` (PyPI, distinct from repo name)
- **Version**: Single source in `pyproject.toml:7`
- **Build system**: `setuptools` with `src/` layout
- **Data files**: Includes `*.jsonl` from `biz/dfch/asdste100mcp/data/` + `py.typed` marker

## Entry Points

- **CLI command**: `ste100-mcp` (typer CLI app defined in `cli.py`)
- **Module entry**: `python -m biz.dfch.asdste100mcp` (runs `__main__.py`, which invokes `cli.app()`)
