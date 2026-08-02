# Copyright (C) 2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""MCP server for the ASD-STE100 Issue 9 vocabulary and rules.

Exposes six read-only tools backed by the local ``biz-dfch-asdste100vocab``
and ``biz-dfch-asdste100nlp`` libraries, and eight read-only tools backed by
the local ``biz-dfch-asdste100rules`` library — no network calls are made at
tool-invocation time.

Tools
-----
word_find         -- Search for a term by exact name (case-insensitive) in the ASD-STE100 Issue 9 vocabulary. Return approved/rejected status, part of speech, STE examples, and approved alternatives. Use this first when you know the exact word. Use `word_match` with a wildcard if this tool returns no items.
word_match        -- Search the vocabulary using a regular expression pattern. Return all entries whose term matches. Use it to find all words with a common prefix or pattern (e.g. ^de or .*tion$). Paginated (`max_results`/`offset`); returns a `WordResult`.
word_fuzzy        -- Search for a term with sequence-matching (Python difflib.get_close_matches). Results may not be obvious — use when word_find returns nothing and you want suggestions.
word_list         -- Return all vocabulary entries. Only use when you need to process the full vocabulary. Use word_count instead if you only need the total. Paginated (`max_results`/`offset`); returns a `WordResult`.
word_count        -- Return the total number of entries in the vocabulary. Use instead of word_list when you only need the count.
word_synonym      -- Search for vocabulary entries that are WordNet synonyms of a word (via `biz-dfch-asdste100nlp`'s `Nlp` class). Use this to find approved alternatives for a non-STE word.
rules_find        -- Search for rules by exact id (e.g. 'R1.1', 'GR-8').
rules_match       -- Search rules using a regular expression over name and summary.
rules_search      -- Full-text search rules, including every content block (notes, examples, technical noun/verb lists, ...). Paginated (`max_results`/`offset`); returns a `SearchResult`.
rules_by_section  -- Search for rules by exact section name.
rules_by_category -- Search for rules by exact category name.
rules_examples    -- Return content items across rules, optionally scoped and filtered. Paginated (`max_results`/`offset`); returns a `RulesExamplesResult`.
rules_overview    -- Return a lightweight, per-rule overview of the ruleset.
rules_toc         -- Return the distinct (section, category) pairs as a table-of-contents outline.

Resources
---------
asdste100://rules/toc          -- Table-of-contents outline of the ruleset (mirrors `rules_toc`).
asdste100://rules/rule/{id_}   -- A single rule/recommendation/information item by exact id (mirrors `rules_find`).
asdste100://version            -- Version numbers of the MCP server, vocab, rules, and nlp libraries.
"""  # noqa: E501

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated, Any

from mcp.server import MCPServer
from mcp_types import ToolAnnotations
from pydantic import Field

from biz.dfch.asdste100nlp import Nlp
from biz.dfch.asdste100rules.rules import Rules
from biz.dfch.asdste100vocab import Vocab

from .settings import Factory


# ---------------------------------------------------------------------------
# Shared vocabulary instance (loaded once at startup)
# ---------------------------------------------------------------------------

_vocab: Vocab | None = None  # pylint: disable=invalid-name


def _get_vocab() -> Vocab:
    assert _vocab is not None, "Vocab not initialised — lifespan did not run."
    return _vocab


# ---------------------------------------------------------------------------
# Shared rules instance (loaded once at startup)
# ---------------------------------------------------------------------------

_rules: Rules | None = None  # pylint: disable=invalid-name


def _get_rules() -> Rules:
    assert _rules is not None, "Rules not initialised — lifespan did not run."
    return _rules


# ---------------------------------------------------------------------------
# Shared NLP instance (loaded once at startup)
# ---------------------------------------------------------------------------

_nlp: Nlp | None = None  # pylint: disable=invalid-name


def _get_nlp() -> Nlp:
    assert _nlp is not None, "Nlp not initialised — lifespan did not run."
    return _nlp


# ---------------------------------------------------------------------------
# Lifespan: load vocab, rules, and nlp on startup, release on shutdown
# ---------------------------------------------------------------------------


@asynccontextmanager
async def _lifespan(server: MCPServer) -> AsyncGenerator[dict[str, Any], None]:  # noqa: ARG001
    global _vocab, _rules, _nlp  # pylint: disable=global-statement
    _ = server
    settings = Factory.get_instance()
    _vocab = Vocab(
        files=settings.vocab_files,
        use_ste100=settings.use_asdste100_vocab,
        use_ste100_technical_word=settings.use_asdste100_technical_words,
    )
    _rules = Rules(
        files=settings.rules_files,
        use_builtin=settings.use_asdste100_rules,
    )
    _nlp = Nlp(_vocab)
    try:
        yield {}
    finally:
        _vocab = None
        _rules = None
        _nlp = None


# ---------------------------------------------------------------------------
# MCPServer application
# ---------------------------------------------------------------------------

mcp = MCPServer(
    name="asdste100-mcp",
    instructions="Search ASD-STE100 Issue 9 vocabulary and rules entries.",
    lifespan=_lifespan,
)

_READ_ONLY = ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    open_world_hint=False,
)

_Term = Annotated[str, Field(min_length=1, max_length=200, description="The term to look up.")]

# ---------------------------------------------------------------------------
# Tool and resource registration (side-effects: registers all tools and
# resources on mcp).
# ---------------------------------------------------------------------------

from . import resources, tools  # noqa: E402, F401
