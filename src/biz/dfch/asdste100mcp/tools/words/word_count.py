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

"""Tool: word_count — return the total number of entries in the ASD-STE100 Issue 9 vocabulary."""

from __future__ import annotations

from ...server import _READ_ONLY, _get_vocab, mcp


@mcp.tool(annotations=_READ_ONLY)
def word_count() -> int:
    """
    Return the total number of entries in the vocabulary.

    Use instead of `word_list` when you only need the count.

    Returns
    -------
    int
        The number of entries in the vocabulary.
    """

    return len(_get_vocab())
