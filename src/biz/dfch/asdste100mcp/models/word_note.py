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

"""Pydantic model mirroring :class:`~biz.dfch.asdste100vocab.WordNote`."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class WordNote(BaseModel):
    """Pydantic equivalent of :class:`biz.dfch.asdste100vocab.WordNote`.

    Parameters matching the source dataclass
    ----------------------------------------
    value:
        The note text, if any.
    words:
        Cross-referenced words (kept as plain dicts to avoid circular imports).
    ste_example:
        An example of accepted STE usage, if any.
    nonste_example:
        An example of rejected (non-STE) usage, if any.
    """

    value: str | None = None
    words: list[dict[str, Any]] = []
    ste_example: str | None = None
    nonste_example: str | None = None
