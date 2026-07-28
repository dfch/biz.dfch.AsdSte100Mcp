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

"""Pydantic model mirroring :class:`~biz.dfch.asdste100vocab.Word`."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .word_meaning import WordMeaning
from .word_note import WordNote


class Word(BaseModel):
    """Pydantic equivalent of :class:`biz.dfch.asdste100vocab.Word`.

    Parameters matching the source dataclass
    ----------------------------------------
    name:
        The word itself.
    status:
        ``approved``, ``rejected``, or ``unknown``.
    word_type:
        Part-of-speech tag (e.g. ``n``, ``v``, ``adj``).  The source
        dataclass names this field ``type_`` (trailing underscore to avoid
        shadowing the built-in :data:`type`); the alias ``type_`` is
        accepted at validation time so that dicts produced by
        ``Vocab._word_to_dict()`` validate without transformation.
    meanings:
        One or more ASD-STE100 definitions for this word.
    spellings:
        Alternate acceptable spellings, if any.
    alternatives:
        Synonyms or cross-references.  Typed as ``list[Word]`` — Pydantic
        resolves the forward reference after the class is fully defined.
    source:
        Original dictionary source identifier.
    category:
        Category code from the STE100 standard.
    ste_example:
        Examples showing accepted STE usage.
    nonste_example:
        Examples of rejected (non-STE) usage.
    note:
        A descriptive note, if present.
    """

    name: str
    status: str = ""
    word_type: str = Field("", alias="type_")
    meanings: list[WordMeaning] = Field(default_factory=list)
    spellings: list[str] = Field(default_factory=list)
    alternatives: list[Word] = Field(default_factory=list)
    source: str = ""
    category: str = ""
    ste_example: list[str] = Field(default_factory=list)
    nonste_example: list[str] = Field(default_factory=list)
    note: WordNote | None = None

    model_config = {
        "populate_by_name": True,
    }
