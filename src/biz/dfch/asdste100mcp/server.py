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
find    -- Search for a term by exact name (case-insensitive) in the ASD-STE100 Issue 9 vocabulary. Return approved/rejected status, part of speech, STE examples, and approved alternatives. Use this first when you know the exact word. Use `asdste100_match` with a wildcard if this tool returns no items.
match   -- Search the vocabulary using a regular expression pattern. Return all entries whose term matches. Return all entries whose term matches. Use it to find all words with a common prefix or pattern (e.g. ^de or .*tion$).
similar -- Search for a term with sequence-matching (Python difflib.get_close_matches). Results may not be obvious — use when find returns nothing and you want suggestions.
list    -- Return all vocabulary entries. Only use when you need to process the full vocabulary. Use asdste100_count instead if you only need the total. This operation is expensive and return a large number of text.
count   -- Return the total number of entries in the vocabulary. Use instead of asdste100_list when you only need the count.
"""  # noqa: E501

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated, Any

from mcp.server import MCPServer
from mcp_types import ToolAnnotations
from pydantic import Field

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
# Lifespan: load vocab on startup, release on shutdown
# ---------------------------------------------------------------------------


@asynccontextmanager
async def _lifespan(server: MCPServer) -> AsyncGenerator[dict[str, Any], None]:  # noqa: ARG001
    global _vocab  # pylint: disable=global-statement
    _ = server
    settings = Factory.get_instance()
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
    instructions="Search ASD-STE100 Issue 9 vocabulary entries.",
    lifespan=_lifespan,
)

_READ_ONLY = ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    open_world_hint=False,
)

_Term = Annotated[str, Field(min_length=1, max_length=200, description="The term to look up.")]

# ---------------------------------------------------------------------------
# Tool registration (side-effects: registers all tools on mcp).
# ---------------------------------------------------------------------------

from . import tools  # noqa: E402, F401
