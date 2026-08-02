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

"""Resource template: asdste100://rules/rule/{id_} — a single rule by exact id."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from biz.dfch.asdste100rules.models import Rule

from ...server import _get_rules, mcp

_RuleId = Annotated[
    str,
    Field(
        min_length=1,
        max_length=200,
        description="The exact rule/recommendation id to look up, e.g. 'R1.1' or 'GR-8' (case-insensitive).",
    ),
]


@mcp.resource(
    "asdste100://rules/rule/{id_}",
    name="rules_find",
    title="ASD-STE100 Rule",
    description=(
        "A single rule/recommendation/information item from the ASD-STE100 Issue 9 ruleset, looked "
        "up by its exact id (e.g. 'R1.1' or 'GR-8'). Lets a client attach one specific rule as "
        "context (e.g. via an '@mention' or resource picker) without a tool round-trip. Mirrors the "
        "`rules_find` tool."
    ),
    mime_type="application/json",
)
def rules_find(id_: _RuleId) -> list[Rule]:
    """
    Return the rule(s) matching an exact id.

    Matching is case-insensitive. An unknown id yields an empty list
    rather than an error, so that reading a not-yet-known rule id is not
    treated as a hard failure.

    Parameters
    ----------
    id_:
        The rule/recommendation id to look up (e.g. ``"R1.1"`` or
        ``"GR-8"``), matched case-insensitively.

    Returns
    -------
    list[Rule]
        A (possibly empty) list of matching rules.
    """

    return _get_rules().find(id_)
