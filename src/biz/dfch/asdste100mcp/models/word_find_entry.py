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

"""Pydantic model wrapping one term's result within a `word_find_many` call."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .word import Word


class WordFindEntry(BaseModel):
    """The `word_find` result for a single term, as part of a `word_find_many` call.

    Every input term to `word_find_many` gets exactly one `WordFindEntry`
    in the returned list, in the same order the terms were given —
    including terms that match nothing, so callers can always line up
    inputs and outputs positionally without needing a lookup by ``term``.

    Parameters
    ----------
    term:
        The term that was looked up, exactly as given by the caller.
    results:
        The (possibly empty) list of matching vocabulary entries for
        `term` — 0, 1, or more, same as a single `word_find` call would
        return.
    """

    term: str
    results: list[Word] = Field(default_factory=list)
