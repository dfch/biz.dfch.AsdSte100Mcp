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

"""Pydantic model wrapping a paginated `word_list`/`word_match` result."""

from __future__ import annotations

from pydantic import Field

from .paged_result import PagedResult
from .word import Word


class WordResult(PagedResult):
    """A single page of a `word_list`/`word_match` result, with pagination metadata.

    The vocabulary holds thousands of entries, and `word_list` always
    returns every one of them unless paginated; `word_match` can match
    just as many with a broad enough pattern. See `PagedResult` for the
    meaning of `total`, `offset`, `max_results`, and `truncated`.

    Parameters
    ----------
    results:
        The page of matching vocabulary entries, after
        ``offset``/``max_results`` have been applied.
    """

    results: list[Word] = Field(default_factory=list)
