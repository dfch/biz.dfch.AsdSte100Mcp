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

"""Tests for the PagedResult Pydantic base model."""

import unittest

from biz.dfch.asdste100mcp.models import PagedResult


class TestPagedResult(unittest.TestCase):
    """Tests for the PagedResult Pydantic base model."""

    def test_paged_result_holds_fields(self):
        """A PagedResult must store all given fields as-is."""
        paged = PagedResult(total=3, offset=1, max_results=1, truncated=True)
        self.assertEqual(paged.total, 3)
        self.assertEqual(paged.offset, 1)
        self.assertEqual(paged.max_results, 1)
        self.assertTrue(paged.truncated)
