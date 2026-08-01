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

"""Pydantic model wrapping a paginated `rules_search` result."""

from __future__ import annotations

from pydantic import BaseModel, Field

from biz.dfch.asdste100rules.models import Rule


class SearchResult(BaseModel):
    """A single page of a `rules_search` result, with pagination metadata.

    A plain ``list[Rule]`` cannot tell a caller whether a full page of
    ``max_results`` matches means "that's all of them" or "there are more
    -- call again with a higher ``offset``". This wrapper carries the
    counts needed to make that distinction explicit.

    Parameters
    ----------
    results:
        The page of matching rules, after ``offset``/``max_results`` have
        been applied, in document order.
    total:
        The total number of rules that matched the search, before
        pagination was applied.
    offset:
        The ``offset`` that was used to produce this page.
    max_results:
        The ``max_results`` that was used to produce this page.
    truncated:
        ``True`` when ``total`` is greater than ``offset + len(results)``,
        i.e. there are more matches available beyond this page. Query
        again with a higher ``offset`` to retrieve them.
    """

    results: list[Rule] = Field(default_factory=list)
    total: int
    offset: int
    max_results: int
    truncated: bool
