# biz.dfch.AsdSte100Mcp

[![ASD-STE100: Issue 9](https://img.shields.io/badge/ASD--STE100-Issue%209-blue.svg)](https://www.asd-ste100.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![Pylint and unittest](https://github.com/dfch/biz.dfch.AsdSte100Mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/dfch/biz.dfch.AsdSte100Mcp/actions/workflows/ci.yml)
[![TestPyPI version](https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/biz-dfch-asdste100mcp/json&label=TestPyPI&query=$.info.version&color=orange)](https://test.pypi.org/project/biz-dfch-asdste100mcp/)
[![PyPI version](https://img.shields.io/badge/dynamic/json?url=https://www.pypi.org/pypi/biz-dfch-asdste100mcp/json&label=PyPI&query=$.info.version&color=blue)](https://www.pypi.org/project/biz-dfch-asdste100mcp/)
[![PyPI downloads](https://img.shields.io/pypi/dm/biz-dfch-asdste100mcp.svg)](https://pypistats.org/packages/biz-dfch-asdste100mcp)
[![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-8A2BE2.svg)](https://modelcontextprotocol.io/)
[![Auth: none](https://img.shields.io/badge/auth-none-brightgreen.svg)](#architecture-decision)

An MCP server for the ASD-STE100 (Simplified Technical English) Issue 9 vocabulary.

## Tools

| Tool | Description |
|---|---|
| `find`  | Search for a term by exact name (case-insensitive) in the ASD-STE100 Issue 9 vocabulary. Return approved/rejected status, part of speech, STE examples, and approved alternatives. Use this first when you know the exact word. Use `asdste100_match` with a wildcard if this tool returns no items. |
| `match` | Search the vocabulary using a regular expression pattern. Return all entries whose term matches. Return all entries whose term matches. Use it to find all words with a common prefix or pattern (e.g. ^de or .*tion$). |
| `similar` | Search for a term with sequence-matching (Python difflib.get_close_matches). Results may not be obvious — use when find returns nothing and you want suggestions. |
| `list` | Return all vocabulary entries. Only use when you need to process the full vocabulary. Use asdste100_count instead if you only need the total. This operation is expensive and return a large number of text. |
| `count` | Return the total number of entries in the vocabulary. Use instead of asdste100_list when you only need the count. |

## Installation

```bash
pip install biz-dfch-asdste100mcp
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add biz-dfch-asdste100mcp
```

## Usage

### stdio (Claude Desktop, OpenCode, and other MCP hosts)

```bash
ste100-mcp
```

### SSE / network

```bash
ste100-mcp --transport sse --host 127.0.0.1 --port 8000
```

### Options

| Option | Env var | Default | Description |
|---|---|---|---|
| `--transport` | `STE100_MCP_TRANSPORT` | `stdio` | Transport mode: `stdio` or `sse` |
| `--host` | `STE100_MCP_HOST` | `127.0.0.1` | Bind address (SSE only) |
| `--port` | `STE100_MCP_PORT` | `8000` | TCP port (SSE only) |
| `--env` | — | auto-discovered | Path to a `.env` file |

### Vocabulary configuration

| Env var | Default | Description |
|---|---|---|
| `STE100_MCP_FILES` | _(empty)_ | Colon-separated paths to additional vocabulary files |
| `STE100_MCP_USE_STE100` | `true` | Load the built-in ASD-STE100 Issue 9 vocabulary |
| `STE100_MCP_USE_STE100_TECHNICAL_WORDS` | `false` | Also load the technical words vocabulary |

### OpenCode Configuration


## Adding ASD-STE100 MCP Server to OpenCode

To add the ASD-STE100 (Simplified Technical English) MCP server to your OpenCode configuration:

1. Open your OpenCode config file (typically `~/.config/opencode/opencode.json` or `~/.config/opencode/opencode.jsonc`)

2. Add the following configuration to the `mcp` section (and use it via `stdio`):

```json
"asdste100": {
  "type": "local",
  "enabled": true,
  "command": ["uvx", "--from", "biz-dfch-asdste100mcp", "ste100-mcp"]
}
```

3. Save the file and restart OpenCode

This enables OpenCode to access ASD-STE100 vocabulary lookups for technical writing and documentation compliance.

## Development

### Install dev dependencies

```bash
uv sync --all-extras
```

### Run linters

```bash
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py')
```

### Run tests

```bash
uv run --frozen python -m unittest discover -v -s tests -t . -p "test_*.py"
```

## Make a Release

### 1. Make sure all tests pass

Before releasing, make sure the CI pipeline is green on the `dev` branch:

```bash
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py')
uv run --frozen python -m unittest discover -v -s tests -t . -p "test_*.py"
```

### 2. Increase the version

Update the version in `pyproject.toml`:

```toml
version = "x.y.z"
```

### 3. Commit and push to `dev`

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to vx.y.z"
git push origin dev
```

### 4. Merge `dev` into `main`

```bash
git checkout main
git merge dev
git push origin main
```

### 5. Create and push a version tag

```bash
export VERSION=x.y.z
git tag v${VERSION}
git push origin v${VERSION}
```

Pushing the tag triggers the `publish.yml` workflow, which will:

1. Build the sdist and wheel.
2. Publish to **TestPyPI** (environment `testpypi`).
3. Publish to **PyPI** (environment `pypi`), only if TestPyPI succeeded.
4. Create a **GitHub Release** with auto-generated notes and the distribution artifacts attached.

Then switch back to `dev` to continue work:

```bash
git checkout dev
```

### Configure Trusted Publishing

The workflow uses OIDC Trusted Publishing — no API tokens or secrets are needed.

#### GitHub: create environments

Go to your repo → **Settings** → **Environments** and create two environments:

| Environment | Recommended protection |
|---|---|
| `testpypi` | None required |
| `pypi` | Add a required reviewer to prevent accidental production releases |

#### TestPyPI

Log in at [test.pypi.org](https://test.pypi.org) → **Your account** → **Publishing** → **Add a new pending publisher**:

| Field | Value |
|---|---|
| PyPI project name | `biz-dfch-asdste100mcp` |
| Owner | `dfch` |
| Repository | `biz.dfch.AsdSte100Mcp` |
| Workflow name | `publish.yml` |
| Environment | `testpypi` |

#### PyPI

Log in at [pypi.org](https://pypi.org) → **Your account** → **Publishing** → **Add a new pending publisher**:

| Field | Value |
|---|---|
| PyPI project name | `biz-dfch-asdste100mcp` |
| Owner | `dfch` |
| Repository | `biz.dfch.AsdSte100Mcp` |
| Workflow name | `publish.yml` |
| Environment | `pypi` |

## License

[AGPL-3.0-or-later](LICENSE)
