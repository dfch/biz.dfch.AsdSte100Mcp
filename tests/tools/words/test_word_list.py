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

"""Tests for the word_list tool."""

import unittest

from biz.dfch.asdste100mcp import server
from biz.dfch.asdste100mcp.tools.words.word_list import word_list
from biz.dfch.asdste100vocab import Vocab


class TestWordListToolPagination(unittest.TestCase):
    """Tests for the `max_results`/`offset` pagination of the word_list tool."""

    def setUp(self):
        server._vocab = Vocab()  # pylint: disable=protected-access

    def tearDown(self):
        server._vocab = None  # pylint: disable=protected-access

    def test_default_max_results_returns_first_page(self):
        """With no pagination arguments, the tool must return the first page (up to the default cap)."""
        total = len(server._get_vocab().as_dict())  # pylint: disable=protected-access
        result = word_list()
        self.assertEqual(len(result.results), 25)
        self.assertEqual(result.total, total)
        self.assertEqual(result.offset, 0)
        self.assertEqual(result.max_results, 25)
        self.assertTrue(result.truncated)

    def test_max_results_limits_the_number_of_results(self):
        """`max_results` must cap the number of returned vocabulary entries."""
        result = word_list(max_results=1)
        self.assertEqual(len(result.results), 1)
        self.assertTrue(result.truncated)

    def test_max_results_covering_all_entries_reports_not_truncated(self):
        """When the page covers every entry, `truncated` must be False even at the cap."""
        total = len(server._get_vocab().as_dict())  # pylint: disable=protected-access
        result = word_list(max_results=total)
        self.assertEqual(len(result.results), total)
        self.assertFalse(result.truncated)

    def test_offset_beyond_results_returns_empty_list_but_reports_total(self):
        """An `offset` past the end of the results must return an empty page, not truncated, with the true total."""
        total = len(server._get_vocab().as_dict())  # pylint: disable=protected-access
        result = word_list(max_results=total, offset=total + 1)
        self.assertEqual(result.results, [])
        self.assertEqual(result.total, total)
        self.assertFalse(result.truncated)
