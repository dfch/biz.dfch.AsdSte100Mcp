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

"""Pydantic model for the ``asdste100://version`` resource."""

from __future__ import annotations

from pydantic import BaseModel


class VersionInfo(BaseModel):
    """Installed version numbers of the MCP server and its data libraries.

    Parameters
    ----------
    mcp:
        Version of this ``biz-dfch-asdste100mcp`` package.
    vocab:
        Version of the ``biz-dfch-asdste100vocab`` vocabulary library.
    rules:
        Version of the ``biz-dfch-asdste100rules`` ruleset library.
    nlp:
        Version of the ``biz-dfch-asdste100nlp`` nlp library.
    """

    mcp: str
    vocab: str
    rules: str
    nlp: str
