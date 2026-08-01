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

"""Tool: rules_by_section — exact section-name search in the ASD-STE100 Issue 9 ruleset."""

from __future__ import annotations

from biz.dfch.asdste100rules.models import Rule

from ...server import _READ_ONLY, _get_rules, mcp
from ._params import Section


@mcp.tool(annotations=_READ_ONLY)
def rules_by_section(section: Section) -> list[Rule]:
    """
    Search for rules in the ruleset by exact section name (case-insensitive).

    Use `rules_toc` first if you do not know the exact section names.

    Parameters
    ----------
    section:
        The section name to search for, e.g. ``"Words"``.

    Returns
    -------
    list[Rule]
        A (possibly empty) list of matching rules.
    """

    return _get_rules().by_section(section)
