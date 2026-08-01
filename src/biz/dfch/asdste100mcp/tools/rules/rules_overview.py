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

"""Tool: rules_overview — lightweight, per-rule overview of the ruleset."""

from __future__ import annotations

from biz.dfch.asdste100rules.models import RuleOverview

from ...server import _READ_ONLY, _get_rules, mcp
from ._params import Brief, EntryTypeParam, OptionalCategory, OptionalSection


@mcp.tool(annotations=_READ_ONLY)
def rules_overview(
    section: OptionalSection = None,
    category: OptionalCategory = None,
    type_: EntryTypeParam = None,
    brief: Brief = True,
) -> list[RuleOverview]:
    """
    Return a lightweight, per-rule overview of the ruleset.

    Use this for a cheap, low-token summary of what rules exist before
    drilling into `rules_find` or `rules_examples` for a specific rule;
    each result carries only the rule's id, type, section, category,
    name, and (optionally) summary, plus counts/flags about its content
    items rather than the content items themselves.

    Parameters
    ----------
    section:
        When given, only consider rules in this exact section
        (case-insensitive).
    category:
        When given, only consider rules in this exact category
        (case-insensitive).
    type_:
        When given, only consider rules of this exact type (e.g.
        ``"rule"``, to exclude recommendations and informational
        blocks).
    brief:
        When ``True`` (default), omit the summary to keep the payload
        small. When ``False``, include the full summary.

    Returns
    -------
    list[RuleOverview]
        One overview per matching rule, in the ruleset's current order
        (natural id order by default).
    """

    return _get_rules().overview(section=section, category=category, type_=type_, brief=brief)
