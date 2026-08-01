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

"""Pydantic model wrapping a ``Rules.toc()`` result tuple."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TocEntry(BaseModel):
    """One ``(section, category, ids)`` entry from ``Rules.toc()``.

    A thin pydantic wrapper around the plain ``tuple[str, str, list[str]]``
    returned by :meth:`biz.dfch.asdste100rules.rules.Rules.toc` — tuples do
    not have a natural JSON-schema shape for an MCP tool response, so each
    tuple is converted to one ``TocEntry`` instance.

    Parameters
    ----------
    section:
        The section name, e.g. ``"Words"``.
    category:
        The category name within that section, e.g. ``"Technical nouns"``.
    ids:
        The ids of every rule/recommendation/information item in this
        (section, category) pair, in document order.
    """

    section: str
    category: str
    ids: list[str] = Field(default_factory=list)
