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

"""Resource: asdste100://rules/toc — table-of-contents outline of the ruleset."""

from __future__ import annotations

from ...models import TocEntry
from ...server import _get_rules, mcp


@mcp.resource(
    "asdste100://rules/toc",
    name="rules_toc",
    title="ASD-STE100 Rules — Table of Contents",
    description=(
        "The distinct (section, category) pairs of the ASD-STE100 Issue 9 ruleset, in first-seen "
        "document order, each with the ids of every rule/recommendation/information item it "
        "contains. Lets a client browse the ruleset's structure (e.g. in a tree view) without a "
        "tool round-trip. Mirrors the `rules_toc` tool with no `section` filter."
    ),
    mime_type="application/json",
)
def rules_toc() -> list[TocEntry]:
    """
    Return the full table-of-contents outline of the ruleset.

    Returns
    -------
    list[TocEntry]
        One entry per distinct (section, category) pair, in first-seen
        document order, where ``ids`` lists the ids of every
        rule/recommendation/information item in that (section, category),
        in document order.
    """

    pairs = _get_rules().toc()
    return [TocEntry(section=section, category=category, ids=ids) for section, category, ids in pairs]
