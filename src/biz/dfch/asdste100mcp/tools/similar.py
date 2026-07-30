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

"""Tool: similar — sequence matching search in the ASD-STE100 Issue 9 vocabulary."""

from __future__ import annotations

from biz.dfch.asdste100vocab import Vocab

from ..models import Word
from ..server import _READ_ONLY, _Term, _get_vocab, mcp


@mcp.tool(annotations=_READ_ONLY)
def similar(term: _Term) -> list[Word]:
    """
    Search for a term with sequence-matching (Python difflib.get_close_matches).

    Results may not be obvious — use when find returns nothing and you want
    suggestions.

    Parameters
    ----------
    term:
        The word or phrase to search for approximately.

    Returns
    -------
    list[Word]
        A (possibly empty) list of similar vocabulary entries.
    """

    words = _get_vocab().similar(term)
    result = [Word.model_validate(Vocab._word_to_dict(w)) for w in words]  # pylint: disable=protected-access
    return result
