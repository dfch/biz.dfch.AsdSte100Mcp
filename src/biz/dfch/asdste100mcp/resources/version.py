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

"""Resource: asdste100://version — server and data-library version numbers."""

from __future__ import annotations

from importlib.metadata import version

from ..models import VersionInfo
from ..server import mcp


@mcp.resource(
    "asdste100://version",
    name="version",
    title="ASD-STE100 MCP Server Version",
    description=(
        "Installed version numbers of the ASD-STE100 MCP server itself and its three "
        "data-backing libraries: biz-dfch-asdste100vocab (vocabulary), "
        "biz-dfch-asdste100rules (ruleset), and biz-dfch-asdste100nlp (synonyms). "
        "Lets a client check compatibility without a tool round-trip."
    ),
    mime_type="application/json",
)
def version_info() -> VersionInfo:
    """
    Return the installed version numbers of the server and its data libraries.

    Returns
    -------
    VersionInfo
        The version of this ``biz-dfch-asdste100mcp`` package, plus the
        versions of ``biz-dfch-asdste100vocab``, ``biz-dfch-asdste100rules``,
        and ``biz-dfch-asdste100nlp`` as currently installed.
    """

    return VersionInfo(
        mcp=version("biz-dfch-asdste100mcp"),
        vocab=version("biz-dfch-asdste100vocab"),
        rules=version("biz-dfch-asdste100rules"),
        nlp=version("biz-dfch-asdste100nlp"),
    )
