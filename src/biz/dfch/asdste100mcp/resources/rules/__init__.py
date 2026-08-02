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

"""MCP resource registrations for the ASD-STE100 Issue 9 rules server.

Each sub-module registers one resource (or resource template) against the
shared ``mcp`` application instance.  Import this package to load all
rules resources at once::

    from biz.dfch.asdste100mcp.resources import rules  # noqa: F401 (side-effects only)
"""

from . import rules_find, rules_toc  # noqa: F401

__all__ = [
    "rules_find",
    "rules_toc",
]
