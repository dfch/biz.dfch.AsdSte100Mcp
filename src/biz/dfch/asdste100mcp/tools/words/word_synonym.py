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

"""Tool: word_synonym — WordNet-based synonym search in the ASD-STE100 Issue 9 vocabulary."""

from __future__ import annotations

from biz.dfch.asdste100vocab import Vocab

from ...models import Word
from ...server import _READ_ONLY, _Term, _get_nlp, mcp


@mcp.tool(annotations=_READ_ONLY)
def word_synonym(term: _Term) -> list[Word]:
    """
    Search for vocabulary entries that are WordNet synonyms of a word (via
    the `biz-dfch-asdste100nlp` library's `Nlp` class).

    Every WordNet synset for `term` is collected and its lemma names are
    cross-referenced, case-insensitively, against the vocabulary's entries
    by name — the same scope as `word_find`/`word_match`/`word_fuzzy`
    (approved and rejected entries both included). `term` itself is
    excluded from the result. Use this to find approved alternatives for a
    non-STE word.

    Parameters
    ----------
    term:
        The word to search synonyms for.

    Returns
    -------
    list[Word]
        A deduplicated, alphabetically sorted list of matching vocabulary
        entries. Empty if `term` has no WordNet synsets (out-of-
        vocabulary) or none of its synonyms are present in the vocabulary.
    """

    words = _get_nlp().synonym(term)
    result = [Word.model_validate(Vocab._word_to_dict(w)) for w in words]  # pylint: disable=protected-access
    return result
