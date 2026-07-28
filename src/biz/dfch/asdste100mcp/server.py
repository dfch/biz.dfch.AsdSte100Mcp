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

"""MCP server for the ASD-STE100 Issue 9 vocabulary.

Exposes five read-only tools backed by the local ``biz-dfch-ste100vocab``
library — no network calls are made at tool-invocation time.

Tools
-----
find    -- exact term lookup; returns matching entries.
match   -- regex match against terms; returns matching entries.
similar -- fuzzy / prefix lookup; returns matching entries.
list    -- return all entries in the vocabulary.
count   -- return the total number of entries in the vocabulary.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated, Any

from mcp.server import MCPServer
from mcp_types import ToolAnnotations
from pydantic import Field

from biz.dfch.asdste100vocab import Vocab

from .models import Word
from .settings import Settings


# ---------------------------------------------------------------------------
# Shared vocabulary instance (loaded once at startup)
# ---------------------------------------------------------------------------

_vocab: Vocab | None = None  # pylint: disable=invalid-name


def _get_vocab() -> Vocab:
    assert _vocab is not None, "Vocab not initialised — lifespan did not run."
    return _vocab


# ---------------------------------------------------------------------------
# Lifespan: load vocab on startup, release on shutdown
# ---------------------------------------------------------------------------


@asynccontextmanager
async def _lifespan(server: MCPServer) -> AsyncGenerator[dict[str, Any], None]:  # noqa: ARG001
    global _vocab  # pylint: disable=global-statement
    _ = server
    settings = Settings()
    _vocab = Vocab(
        files=settings.files,
        use_ste100=settings.use_ste100,
        use_ste100_technical_word=settings.use_ste100_technical_words,
    )
    try:
        yield {}
    finally:
        _vocab = None


# ---------------------------------------------------------------------------
# MCPServer application
# ---------------------------------------------------------------------------

mcp = MCPServer(
    name="ste100-mcp",
    instructions="Look up ASD-STE100 Issue 9 vocabulary entries.",
    lifespan=_lifespan,
)

_READ_ONLY = ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    open_world_hint=False,
)

_Term = Annotated[str, Field(min_length=1, max_length=200, description="The term to look up.")]


# ---------------------------------------------------------------------------
# Tool 1 — find
# ---------------------------------------------------------------------------


@mcp.tool(annotations=_READ_ONLY)
def find(term: _Term) -> list[Word]:
    """Find a term by exact match.

    Performs a case-insensitive exact lookup of *term* in the ASD-STE100
    Issue 9 vocabulary and returns all matching entries.

    Parameters
    ----------
    term:
        The word or phrase to look up exactly.

    Returns
    -------
    list[Word]
        A (possibly empty) list of matching vocabulary entries.
    """

    words = _get_vocab().find(term)
    result = [Word.model_validate(Vocab._word_to_dict(w)) for w in words]  # pylint: disable=protected-access
    return result


# ---------------------------------------------------------------------------
# Tool 2 — match
# ---------------------------------------------------------------------------


@mcp.tool(annotations=_READ_ONLY)
def match(term: _Term) -> list[Word]:
    """Match terms using a regular expression.

    Applies *term* as a regular expression pattern against all entries in
    the ASD-STE100 Issue 9 vocabulary and returns every entry whose term
    field matches.

    Parameters
    ----------
    term:
        A regular-expression pattern (e.g. ``"util.*"``).

    Returns
    -------
    list[Word]
        A (possibly empty) list of matching vocabulary entries.
    """

    words = _get_vocab().match(term)
    result = [Word.model_validate(Vocab._word_to_dict(w)) for w in words]  # pylint: disable=protected-access
    return result


# ---------------------------------------------------------------------------
# Tool 3 — similar
# ---------------------------------------------------------------------------


@mcp.tool(annotations=_READ_ONLY)
def similar(term: _Term) -> list[Word]:
    """Find terms similar to the given term.

    Performs a fuzzy / prefix lookup of *term* in the ASD-STE100 Issue 9
    vocabulary and returns entries that are similar to the query, useful
    when the exact spelling is unknown.

    Parameters
    ----------
    term:
        The word or phrase to search for approximately.

    Returns
    -------
    list[Word]
        A (possibly empty) list of similar vocabulary entries.
    """

    words = _get_vocab().similar(term)
    result = [Word.model_validate(Vocab._word_to_dict(w)) for w in words]  # pylint: disable=protected-access
    return result


# ---------------------------------------------------------------------------
# Tool 4 — list
# ---------------------------------------------------------------------------


@mcp.tool(name="list", annotations=_READ_ONLY)
def list_vocab() -> list[Word]:
    """List all entries in the ASD-STE100 Issue 9 vocabulary.

    Returns the complete vocabulary as a list of entry dicts.  Use
    ``count`` first if you only need the total number of entries.

    Returns
    -------
    list[Word]
        All vocabulary entries.
    """

    words = _get_vocab().as_dict()
    result = [Word.model_validate(w) for w in words]
    return result


# ---------------------------------------------------------------------------
# Tool 5 — count
# ---------------------------------------------------------------------------


@mcp.tool(name="count", annotations=_READ_ONLY)
def count_vocab() -> int:
    """Return the total number of entries in the ASD-STE100 Issue 9 vocabulary.

    Returns
    -------
    int
        The number of entries in the vocabulary.
    """

    return len(_get_vocab())
