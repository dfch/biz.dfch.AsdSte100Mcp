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

"""Tool: rules_examples — content items across rules, optionally scoped and filtered."""

from __future__ import annotations

from ...models import RulesExamplesResult
from ...server import _READ_ONLY, _get_rules, mcp
from .._pagination import MaxResults, Offset, paginate
from ._params import Kind, OptionalCategory, OptionalId, OptionalSection


@mcp.tool(annotations=_READ_ONLY)
def rules_examples(
    id_: OptionalId = None,
    section: OptionalSection = None,
    category: OptionalCategory = None,
    kind: Kind = None,
    max_results: MaxResults = 25,
    offset: Offset = 0,
) -> RulesExamplesResult:
    """
    Return content items across rules, optionally scoped and filtered.

    Parameters
    ----------
    id_:
        When given, only consider the rule with this exact id
        (case-insensitive).
    section:
        When given, only consider rules in this exact section
        (case-insensitive).
    category:
        When given, only consider rules in this exact category
        (case-insensitive).
    kind:
        When given, only return content items of this type (e.g.
        ``"ste_example"``).
    max_results:
        The maximum number of matching content items to return (default 25).
    offset:
        The number of matching content items to skip before returning
        results, for pagination (default 0).

    Returns
    -------
    RulesExamplesResult
        ``results`` holds the (possibly empty) page of matching content
        items, in document order, after applying ``offset`` and
        ``max_results``. ``total`` is the full match count before
        pagination, and ``truncated`` tells the caller whether more
        content items exist beyond this page. Unfiltered, the ruleset
        can hold well over a thousand content items, so pagination
        matters here even though the ruleset itself only has a few
        dozen rules.
    """

    matches = _get_rules().examples(id_=id_, section=section, category=category, kind=kind)
    page, total, truncated = paginate(matches, offset, max_results)
    return RulesExamplesResult(
        results=page,
        total=total,
        offset=offset,
        max_results=max_results,
        truncated=truncated,
    )
