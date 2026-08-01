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

"""Tool: rules_search — full-text regular-expression search across all rule content."""

from __future__ import annotations

from ...models import SearchResult
from ...server import _READ_ONLY, _get_rules, mcp
from .._pagination import MaxResults, Offset, paginate
from ._params import ContentTypes, SearchPattern


@mcp.tool(annotations=_READ_ONLY)
def rules_search(
    pattern: SearchPattern,
    content_types: ContentTypes = None,
    max_results: MaxResults = 25,
    offset: Offset = 0,
) -> SearchResult:
    """
    Full-text search for rules using a regular expression.

    Unlike `rules_match`, which only looks at ``name`` and ``summary``,
    this searches every text a rule carries: ``section``, ``category``,
    ``name``, ``summary``, and the ``data`` of every content item --
    i.e. explanatory text, notes, STE/non-STE examples, technical
    noun/verb lists, and so on. Useful for finding "what rule governs
    passive voice" or "where does STE100 mention abbreviations", without
    knowing the section/category/id upfront.

    Parameters
    ----------
    pattern:
        The regular expression pattern to search for (case-insensitive).
    content_types:
        When given, only the ``data`` of content items whose type is in
        this list is searched (``section``, ``category``, ``name``, and
        ``summary`` are always searched regardless). Use this to narrow
        the search to, e.g., only ``note`` or ``ste_example`` content.
    max_results:
        The maximum number of matching rules to return (default 25).
    offset:
        The number of matching rules to skip before returning results,
        for pagination (default 0).

    Returns
    -------
    SearchResult
        ``results`` holds the (possibly empty) page of matching rules,
        in document order, after applying ``offset`` and ``max_results``.
        ``total`` is the full match count before pagination, and
        ``truncated`` tells the caller whether more matches exist beyond
        this page -- i.e. whether a reached ``max_results`` means "that's
        all of them" or "call again with a higher ``offset``".
    """

    matches = _get_rules().search(pattern, content_types=content_types)
    page, total, truncated = paginate(matches, offset, max_results)
    return SearchResult(
        results=page,
        total=total,
        offset=offset,
        max_results=max_results,
        truncated=truncated,
    )
