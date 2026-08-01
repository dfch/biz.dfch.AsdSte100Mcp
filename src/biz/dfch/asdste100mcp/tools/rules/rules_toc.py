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

"""Tool: rules_toc — table-of-contents outline of the ruleset's structure."""

from __future__ import annotations

from ...models import TocEntry
from ...server import _READ_ONLY, _get_rules, mcp
from ._params import OptionalSection


@mcp.tool(annotations=_READ_ONLY)
def rules_toc(section: OptionalSection = None) -> list[TocEntry]:
    """
    Return the distinct (section, category) pairs, in first-seen order.

    Gives a table-of-contents style outline of the ruleset's structure,
    without any per-rule detail; useful to see which sections and
    categories exist before drilling into `rules_overview`,
    `rules_by_section`, or `rules_by_category` for a specific one.

    Parameters
    ----------
    section:
        When given, only consider rules in this exact section
        (case-insensitive).

    Returns
    -------
    list[TocEntry]
        One entry per distinct (section, category) pair, in first-seen
        document order, where ``ids`` lists the ids of every
        rule/recommendation/information item in that (section,
        category), in document order.
    """

    pairs = _get_rules().toc(section=section)
    return [TocEntry(section=section_, category=category, ids=ids) for section_, category, ids in pairs]
