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

"""Shared pagination parameter types and slicing helper for MCP tools.

Used by any ``rules_*``/``word_*`` tool whose unpaginated result can grow
large enough that a caller cannot tell, from a full page alone, whether
that page is the whole result or just the first slice of it (see
`biz.dfch.asdste100mcp.models.PagedResult`).
"""

from __future__ import annotations

from typing import Annotated, TypeVar

from pydantic import Field

MaxResults = Annotated[
    int,
    Field(
        default=25,
        ge=1,
        le=100,
        description="The maximum number of matching entries to return.",
    ),
]

Offset = Annotated[
    int,
    Field(
        default=0,
        ge=0,
        description="The number of matching entries to skip before returning results, for pagination.",
    ),
]

_T = TypeVar("_T")


def paginate(items: list[_T], offset: int, max_results: int) -> tuple[list[_T], int, bool]:
    """
    Slice ``items`` into a single page and report pagination metadata.

    Parameters
    ----------
    items:
        The full, unpaginated list of matching items.
    offset:
        The number of leading items to skip.
    max_results:
        The maximum number of items to include in the page.

    Returns
    -------
    tuple[list[_T], int, bool]
        ``(page, total, truncated)`` where ``page`` is
        ``items[offset : offset + max_results]``, ``total`` is
        ``len(items)``, and ``truncated`` is ``True`` when ``total`` is
        greater than ``offset + len(page)``, i.e. more items exist beyond
        this page.
    """

    page = items[offset : offset + max_results]
    total = len(items)
    truncated = total > offset + len(page)
    return page, total, truncated
