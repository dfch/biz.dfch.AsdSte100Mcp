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

"""Shared pagination-metadata base for paginated MCP tool results."""

from __future__ import annotations

from pydantic import BaseModel


class PagedResult(BaseModel):
    """Pagination metadata shared by every paginated tool result.

    A plain ``list[...]`` cannot tell a caller whether a full page of
    ``max_results`` items means "that's all of them" or "there are more
    -- call again with a higher ``offset``". Tool-specific result models
    (e.g. ``SearchResult``, ``RulesExamplesResult``, ``WordResult``)
    inherit from this class and add their own ``results`` field with the
    appropriate item type.

    Parameters
    ----------
    total:
        The total number of items that matched, before pagination was
        applied.
    offset:
        The ``offset`` that was used to produce this page.
    max_results:
        The ``max_results`` that was used to produce this page.
    truncated:
        ``True`` when ``total`` is greater than ``offset + len(results)``,
        i.e. there are more items available beyond this page. Query again
        with a higher ``offset`` to retrieve them.
    """

    total: int
    offset: int
    max_results: int
    truncated: bool
