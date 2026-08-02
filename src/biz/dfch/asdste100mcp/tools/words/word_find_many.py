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

"""Tool: word_find_many — exact-match search for multiple terms in one call."""

from __future__ import annotations

from biz.dfch.asdste100vocab import Vocab

from ...models import Word, WordFindEntry
from ...server import _READ_ONLY, _Terms, _get_vocab, mcp


@mcp.tool(annotations=_READ_ONLY)
def word_find_many(terms: _Terms) -> list[WordFindEntry]:
    """
    Search for multiple terms by exact name (case-insensitive) in the
    ASD-STE100 Issue 9 vocabulary in a single call.

    Equivalent to calling `word_find` once per term, but avoids one
    tool round-trip per term. Each input term gets its own entry in the
    result, holding 0, 1, or more matching vocabulary entries — an
    unknown or misspelled term simply yields an empty `results` list for
    that entry rather than shrinking the overall result.

    Parameters
    ----------
    terms:
        The words or phrases to look up exactly.

    Returns
    -------
    list[WordFindEntry]
        One entry per input term, in the same order as `terms`, each
        holding the term and its (possibly empty) list of matching
        vocabulary entries.
    """

    vocab = _get_vocab()
    result = []
    for term in terms:
        words = vocab.find(term)
        matches = [Word.model_validate(Vocab._word_to_dict(w)) for w in words]  # pylint: disable=protected-access
        result.append(WordFindEntry(term=term, results=matches))
    return result
