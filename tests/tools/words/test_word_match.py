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

"""Tests for the word_match tool."""

import unittest

from biz.dfch.asdste100mcp import server
from biz.dfch.asdste100mcp.tools.words.word_match import word_match
from biz.dfch.asdste100vocab import Vocab


class TestWordMatch(unittest.TestCase):
    """Tests for the word_match tool."""

    def setUp(self):
        self.vocab = Vocab()

    def test_match_pattern_returns_results(self):
        """A regex pattern matching known words must return results."""
        result = self.vocab.match("use.*")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_match_non_matching_pattern_returns_empty_list(self):
        """A regex pattern that matches nothing must return an empty list."""
        result = self.vocab.match("zzznonsense.*")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class TestWordMatchToolPagination(unittest.TestCase):
    """Tests for the `max_results`/`offset` pagination of the word_match tool."""

    def setUp(self):
        server._vocab = Vocab()  # pylint: disable=protected-access

    def tearDown(self):
        server._vocab = None  # pylint: disable=protected-access

    def test_default_max_results_matches_unpaginated_match_count(self):
        """With no pagination arguments, the tool must return the first page (up to the default cap)."""
        full = server._get_vocab().match("use.*")  # pylint: disable=protected-access
        result = word_match("use.*")
        self.assertEqual(len(result.results), min(25, len(full)))
        self.assertEqual(result.total, len(full))
        self.assertEqual(result.offset, 0)
        self.assertEqual(result.max_results, 25)

    def test_max_results_limits_the_number_of_results(self):
        """`max_results` must cap the number of returned vocabulary entries."""
        result = word_match("use.*", max_results=1)
        self.assertEqual(len(result.results), 1)

    def test_max_results_reached_before_end_reports_truncated(self):
        """When more matches exist beyond the page, `truncated` must be True."""
        full = server._get_vocab().match("use.*")  # pylint: disable=protected-access
        self.assertGreater(len(full), 1)
        result = word_match("use.*", max_results=1)
        self.assertEqual(result.total, len(full))
        self.assertTrue(result.truncated)

    def test_max_results_covering_all_matches_reports_not_truncated(self):
        """When the page covers every match, `truncated` must be False even at the cap."""
        full = server._get_vocab().match("use.*")  # pylint: disable=protected-access
        result = word_match("use.*", max_results=len(full))
        self.assertEqual(len(result.results), len(full))
        self.assertFalse(result.truncated)

    def test_offset_beyond_results_returns_empty_list_but_reports_total(self):
        """An `offset` past the end of the results must return an empty page, not truncated, with the true total."""
        full = server._get_vocab().match("use.*")  # pylint: disable=protected-access
        result = word_match("use.*", offset=10_000)
        self.assertEqual(result.results, [])
        self.assertEqual(result.total, len(full))
        self.assertFalse(result.truncated)
