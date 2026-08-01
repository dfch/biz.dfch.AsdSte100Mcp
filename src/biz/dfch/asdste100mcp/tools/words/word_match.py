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

"""Tool: word_match — regular-expression search in the ASD-STE100 Issue 9 vocabulary."""

from __future__ import annotations

from biz.dfch.asdste100vocab import Vocab

from ...models import Word, WordResult
from ...server import _READ_ONLY, _Term, _get_vocab, mcp
from .._pagination import MaxResults, Offset, paginate


@mcp.tool(annotations=_READ_ONLY)
def word_match(term: _Term, max_results: MaxResults = 25, offset: Offset = 0) -> WordResult:
    """
    Search the vocabulary using a regular expression pattern.

    Return all entries whose term matches. Use it to find all words with a
    common prefix or pattern (e.g. ^de or .*tion$). A broad pattern can
    match a large part of the vocabulary, so results are paginated.

    Parameters
    ----------
    term:
        A regular-expression pattern (e.g. ``"util.*"``).
    max_results:
        The maximum number of matching vocabulary entries to return
        (default 25).
    offset:
        The number of matching vocabulary entries to skip before
        returning results, for pagination (default 0).

    Returns
    -------
    WordResult
        ``results`` holds the (possibly empty) page of matching
        vocabulary entries after applying ``offset`` and ``max_results``.
        ``total`` is the full match count before pagination, and
        ``truncated`` tells the caller whether more matches exist beyond
        this page.
    """

    matches = _get_vocab().match(term)
    words = [Word.model_validate(Vocab._word_to_dict(w)) for w in matches]  # pylint: disable=protected-access
    page, total, truncated = paginate(words, offset, max_results)
    return WordResult(
        results=page,
        total=total,
        offset=offset,
        max_results=max_results,
        truncated=truncated,
    )
