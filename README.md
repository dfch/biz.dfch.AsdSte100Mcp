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
| `find` | Exact term lookup |
| `match` | Regex pattern match against terms |
| `similar` | Fuzzy / prefix lookup |
| `list` | Return all entries in the vocabulary |
| `count` | Return the total number of entries |

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

## License

[AGPL-3.0-or-later](LICENSE)
