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

from biz.dfch.asdste100rules.models import Rule

from ...server import _READ_ONLY, _get_rules, mcp
from ._params import ContentTypes, SearchPattern


@mcp.tool(annotations=_READ_ONLY)
def rules_search(pattern: SearchPattern, content_types: ContentTypes = None) -> list[Rule]:
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

    Returns
    -------
    list[Rule]
        A (possibly empty) list of matching rules, in document order.
    """

    return _get_rules().search(pattern, content_types=content_types)
