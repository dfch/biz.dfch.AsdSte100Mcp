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

"""Pydantic models mirroring the ASD-STE100 vocab dataclasses, plus small
wrapper models for the ASD-STE100 rules tools.

Usage::

    from biz.dfch.asdste100mcp.models import Word, WordMeaning, WordNote, TocEntry
"""

from .search_result import SearchResult
from .toc_entry import TocEntry
from .word import Word
from .word_meaning import WordMeaning
from .word_note import WordNote

__all__ = [
    "SearchResult",
    "TocEntry",
    "Word",
    "WordMeaning",
    "WordNote",
]
