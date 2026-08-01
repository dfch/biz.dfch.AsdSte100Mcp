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

"""Tool: word_list — return the full ASD-STE100 Issue 9 vocabulary."""

from __future__ import annotations

from ...models import Word
from ...server import _READ_ONLY, _get_vocab, mcp


@mcp.tool(annotations=_READ_ONLY)
def word_list() -> list[Word]:
    """
    Return all vocabulary entries.

    Only use when you need to process the full vocabulary. Use word_count
    instead if you only need the total. This operation is expensive and returns
    a large number of text.

    Returns
    -------
    list[Word]
        All vocabulary entries.
    """

    words = _get_vocab().as_dict()
    result = [Word.model_validate(w) for w in words]
    return result
