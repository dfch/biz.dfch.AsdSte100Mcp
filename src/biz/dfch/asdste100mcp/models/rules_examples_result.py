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

"""Pydantic model wrapping a paginated `rules_examples` result."""

from __future__ import annotations

from pydantic import Field

from biz.dfch.asdste100rules.models import ContentItem

from .paged_result import PagedResult


class RulesExamplesResult(PagedResult):
    """A single page of a `rules_examples` result, with pagination metadata.

    Unfiltered, `rules_examples` can return well over a thousand content
    items across the whole ruleset, so pagination matters even though the
    ruleset itself only holds a few dozen rules. See `PagedResult` for the
    meaning of `total`, `offset`, `max_results`, and `truncated`.

    Parameters
    ----------
    results:
        The page of matching content items, after ``offset``/``max_results``
        have been applied, in document order.
    """

    results: list[ContentItem] = Field(default_factory=list)
