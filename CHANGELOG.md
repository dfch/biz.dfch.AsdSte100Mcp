# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- MCP Registry publishing support via new `publish-to-mcp-registry` GitHub Actions job:
  - Automatically publishes server metadata to the [official MCP Registry](https://registry.modelcontextprotocol.io/)
  - Uses GitHub OIDC authentication (zero secrets, consistent with PyPI Trusted Publishing)
  - Auto-patches `server.json` version fields from git tag at publish time
  - Runs after PyPI publication succeeds in the CI workflow
- `server.json` at repository root defining MCP Registry metadata:
  - Server identity: `io.github.dfch/biz-dfch-asdste100mcp` (GitHub OIDC namespace)
  - PyPI package configuration with `biz-dfch-asdste100mcp` identifier
  - Documentation of all 8 `STE100_MCP_*` environment variables with format hints
  - Conforms to MCP Registry schema v2025-12-11
- PyPI ownership verification marker in README.md long-description for registry discovery

### Changed

- Updated release workflow documentation in README.md to include MCP Registry publishing step
- Added "MCP Registry Publishing" section in README.md with setup and verification instructions
- **Breaking**: Upgraded MCP dependency to version 2.0.0, requiring MCP protocol 2.0 or newer
- **Breaking**: Renamed the `word_similar` vocabulary tool to `word_fuzzy` for clarity
  (`tools/words/word_similar.py` → `tools/words/word_fuzzy.py`). Any caller invoking the
  tool by its previous name must switch to `word_fuzzy`.


## [1.0.0] - 2026-08-01

### Added

- `max_results` (default 25) and `offset` (default 0) pagination parameters
  on `rules_search`, `rules_examples`, `word_list`, and `word_match` --
  the four tools whose unpaginated result can grow large enough (over a
  thousand items, for `rules_examples`; the full multi-thousand-entry
  vocabulary, for `word_list`/`word_match`) that a full page is otherwise
  ambiguous.
- New `PagedResult` base model (`src/biz/dfch/asdste100mcp/models/paged_result.py`)
  carrying the shared `total`, `offset`, `max_results`, and `truncated`
  pagination fields, plus three tool-specific subclasses built on it:
  `SearchResult` (`rules_search`, `results: list[Rule]`),
  `RulesExamplesResult` (`rules_examples`, `results: list[ContentItem]`),
  and `WordResult` (`word_list`/`word_match`, `results: list[Word]`).
  `truncated` tells callers whether a full page means "that's all the
  matches" or "there are more -- call again with a higher `offset`".
- `src/biz/dfch/asdste100mcp/tools/_pagination.py` -- shared `MaxResults`/
  `Offset` parameter types and a `paginate()` slicing helper used by all
  four paginated tools.

### Changed

- **Breaking**: `rules_search` now returns a `SearchResult` object instead
  of a bare `list[Rule]`; the page of matching rules is available at
  `result.results`.
- **Breaking**: `rules_examples` now returns a `RulesExamplesResult`
  object instead of a bare `list[ContentItem]`; the page of matching
  content items is available at `result.results`.
- **Breaking**: `word_list` and `word_match` now return a `WordResult`
  object instead of a bare `list[Word]`; the page of matching vocabulary
  entries is available at `result.results`.

## [0.2.0] - 2026-08-01

### Added

- Eight `rules_*` read-only tools backed by the `biz-dfch-asdste100rules` library:
  `rules_find`, `rules_match`, `rules_search`, `rules_by_section`,
  `rules_by_category`, `rules_examples`, `rules_overview`, `rules_toc`.
  Return types reuse the library's own pydantic models (`Rule`,
  `ContentItem`, `RuleOverview`, `ContentType`, `EntryType`) directly; a
  new `TocEntry` model wraps the plain tuples returned by `Rules.toc()`.
- `--rules-file / -r` CLI option on `ste100-mcp` (repeatable): pass one or
  more rules JSON files at startup, merged with `STE100_MCP_RULES_FILES`.
- `Settings.rules_files` and `Settings.use_ste100_rules` fields;
  `Factory.create_instance(extra_files, extra_rules_files)` now also
  merges rules file paths.
- `tests/tools/rules/` — unit tests for all eight new tools (via `Rules`
  directly, following the existing tool-test convention).
- `tests/models/test_toc_entry.py` — unit tests for the new `TocEntry` model.
- Python 3.14 to the list of supported and CI-tested versions.

### Changed

- Renamed the five vocabulary tools with a `word_` prefix and moved them
  into a new `tools/words/` sub-package: `word_find`, `word_match`,
  `word_similar`, `word_list`, `word_count` (was `find`, `match`,
  `similar`, `list`, `count`). **Breaking**: any caller invoking the
  tools by their previous names must switch to the new `word_*` names.

## [0.1.3] - 2026-07-30

### Changed

- Use new vocab package name: `biz-dfch-asdste100vocab`.

### Doc

- Fix README table formatting (pipe alignment in tool tables).
- Rename CI workflow from "Pylint and unittest" to "Lint and Test".

## [0.1.2] - 2026-07-30

### Added

- `--file / -f` CLI option on `ste100-mcp` (repeatable): pass one or more
  `*.jsonl` vocabulary files at startup.  Paths are merged with those from
  `STE100_MCP_FILES`; duplicates are removed while preserving order.
- `Factory` class in `settings.py` — thread-safe singleton for
  `Settings` using a double-checked lock.  Class-level state removes the
  need for a module-level `global` variable.
  - `Factory.create_instance(extra_files)` — creates the singleton, merges
    CLI-supplied paths with env-supplied paths, asserts it is called only once.
  - `Factory.get_instance()` — returns the singleton, asserts
    `create_instance` was called first.
- `tests/settings/test_factory.py` — 8 unit tests covering singleton
  creation, identity, deduplication, and both `AssertionError` guard paths.

### Changed

- `cli.py` calls `Factory.create_instance(files or [])` before `mcp.run()`
  so CLI-supplied paths are available to the server lifespan.
- `server.py` `_lifespan` calls `Factory.get_instance()` instead of
  constructing a new `Settings()` on every startup.

### Fixed

- Removed bogus `--file` validation block in `cli.py` that called
  `load_dotenv` instead of exiting on error (Typer's `exists=True` already
  rejects non-existent paths).
- Changed `--file` default from mutable `[]` to `None` to avoid the
  mutable-default-argument footgun.

## [0.1.1] - 2026-07-30

### Changed

- Extracted each MCP tool into its own module under the new
  `src/biz/dfch/asdste100mcp/tools/` sub-package (`find.py`, `match.py`,
  `similar.py`, `list.py`, `count.py`).  `server.py` now contains only the
  shared infrastructure (`mcp`, `_lifespan`, `_READ_ONLY`, `_Term`,
  `_get_vocab`) and imports the `tools` package at the bottom to trigger
  registration.  All nine unit tests continue to pass unchanged.
- Moved tool unit tests (`test_find.py`, `test_match.py`, `test_similar.py`,
  `test_count.py`) from `tests/` into the new `tests/tools/` sub-package to
  mirror the source layout.
- Moved `test_word.py` from `tests/` into the new `tests/models/` sub-package
  to mirror the source layout.

## [0.1.0] - 2026-07-28

### Added

- Initial project scaffold for `biz.dfch.AsdSte100Mcp`.
- AGPL-3.0-or-later license and SPDX headers in all Python source files.
- Runtime dependencies: `python-dotenv>=1.2.2`, `mcp`, `typer>=0.12`,
  `pydantic-settings`, `biz-dfch-ste100vocab>=0.7.1`.
- Console script entrypoint `ste100-mcp` pointing to `biz.dfch.asdste100mcp.cli:app`.
- `MCPServer` with five read-only tools: `find`, `match`, `similar`, `list`, `count`;
  backed by the `biz-dfch-ste100vocab` library.
- Typer CLI entry point with `--transport`, `--host`, and `--port` options for
  stdio and SSE transport modes.
- `Settings` class (`settings.py`) reading `STE100_MCP_*` environment variables
  via `pydantic-settings`.
- Pydantic models `Word`, `WordMeaning`, `WordNote` in `models/` package,
  mirroring the vocab library dataclasses.
- Unit tests for all five tools in `tests/` (one file per test class).
- GitHub Actions CI workflow (`ci.yml`) running ruff, pylint, and unit tests
  across Python 3.11, 3.12, and 3.13.
- GitHub Actions publish workflow (`publish.yml`) building and publishing to
  TestPyPI and PyPI on version tags, then creating a GitHub release.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `NOTICE`.
- `CHANGELOG.md` following the Keep a Changelog 1.0.0 format.

### Fixed

- Replaced incorrect `dotenv` dependency with `python-dotenv`.
- Corrected stale `biz.dfch.AsdSte100Vocab` project name references in
  `README.md`, `pyproject.toml`, `cli.py`, `__main__.py`, and `__init__.py`.
- Fixed TOML syntax error (missing comma in `classifiers` array in `pyproject.toml`).
- Removed over-broad `pull-requests: write` permission from CI workflow.
- Pinned `pypa/gh-action-pypi-publish` from floating `release/v1` tag to full
  commit SHA.
- Removed unnecessary single-entry `strategy`/`matrix` from publish workflow jobs.
- Fixed pylint warnings: added missing docstrings, moved `import os` to top level
  in `cli.py`, and added targeted `pylint: disable` comments in `server.py` for
  justified suppressions (`invalid-name`, `global-statement`, `protected-access`).
- Replaced local editable path dependency on `biz-dfch-ste100vocab` with PyPI
  reference to fix CI failure on GitHub Actions runners.
- Let `uv` manage the Python version in CI by passing `python-version` to
  `astral-sh/setup-uv` instead of using `actions/setup-python`.

### Removed

- Removed `main.py` scaffold placeholder; the real entry point is `cli.py`.

[1.0.0]: https://github.com/dfch/biz.dfch.AsdSte100Mcp/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/dfch/biz.dfch.AsdSte100Mcp/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/dfch/biz.dfch.AsdSte100Mcp/compare/v0.1.2...v0.1.3
[Unreleased]: https://github.com/dfch/biz.dfch.AsdSte100Mcp/compare/v1.0.0...HEAD
[0.1.2]: https://github.com/dfch/biz.dfch.AsdSte100Mcp/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/dfch/biz.dfch.AsdSte100Mcp/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dfch/biz.dfch.AsdSte100Mcp/compare/9c36e28...v0.1.0
