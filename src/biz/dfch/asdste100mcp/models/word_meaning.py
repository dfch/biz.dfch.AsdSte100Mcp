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

"""Pydantic model mirroring :class:`~biz.dfch.asdste100vocab.WordMeaning`."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .word_note import WordNote


class WordMeaning(BaseModel):
    """Pydantic equivalent of :class:`biz.dfch.asdste100vocab.WordMeaning`.

    Parameters matching the source dataclass
    ----------------------------------------
    value:
        The defined meaning.
    ste_example:
        Examples showing accepted STE usage for this meaning.
    nonste_example:
        Examples of rejected (non-STE) usage for this meaning.
    note:
        A descriptive note, if present.
    """

    value: str
    ste_example: list[str] = Field(default_factory=list)
    nonste_example: list[str] = Field(default_factory=list)
    note: WordNote | None = None
