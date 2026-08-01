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

"""Tool: rules_match — regular-expression search over rule name/summary."""

from __future__ import annotations

from biz.dfch.asdste100rules.models import Rule

from ...server import _READ_ONLY, _get_rules, mcp
from ._params import RulePattern


@mcp.tool(annotations=_READ_ONLY)
def rules_match(pattern: RulePattern) -> list[Rule]:
    """
    Search for rules in the ruleset using a regular expression.

    The pattern is matched (case-insensitively) against both the ``name``
    and the ``summary`` of each rule. Use `rules_search` instead if you
    need to search the full content of every rule (notes, examples,
    technical noun/verb lists, ...).

    Parameters
    ----------
    pattern:
        The regular expression pattern to search for.

    Returns
    -------
    list[Rule]
        A (possibly empty) list of matching rules.
    """

    return _get_rules().match(pattern)
