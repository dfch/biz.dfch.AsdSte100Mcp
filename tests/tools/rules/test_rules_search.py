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

"""Tests for the rules_search tool."""

import unittest

from biz.dfch.asdste100mcp import server
from biz.dfch.asdste100mcp.tools.rules.rules_search import rules_search
from biz.dfch.asdste100rules.models import ContentType
from biz.dfch.asdste100rules.rules import Rules


class TestRulesSearch(unittest.TestCase):
    """Tests for the rules_search tool."""

    def setUp(self):
        self.rules = Rules()

    def test_search_known_pattern_returns_results(self):
        """Full-text search for a word found only in content blocks must return entries."""
        result = self.rules.search("valve")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_search_unknown_pattern_returns_empty_list(self):
        """Full-text search for a pattern that appears nowhere must return an empty list."""
        result = self.rules.search("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_search_with_content_types_filters_results(self):
        """Restricting to a content type must not return more than the unrestricted search."""
        unrestricted = self.rules.search("valve")
        restricted = self.rules.search("valve", content_types=[ContentType.STE_EXAMPLE])
        self.assertLessEqual(len(restricted), len(unrestricted))


class TestRulesSearchToolPagination(unittest.TestCase):
    """Tests for the `max_results`/`offset` pagination of the rules_search tool."""

    def setUp(self):
        server._rules = Rules()  # pylint: disable=protected-access

    def tearDown(self):
        server._rules = None  # pylint: disable=protected-access

    def test_default_max_results_matches_unpaginated_search(self):
        """With no pagination arguments, the tool must return the full result set (up to the default cap)."""
        full = server._get_rules().search("valve")  # pylint: disable=protected-access
        result = rules_search("valve")
        self.assertEqual(result.results, full[:25])
        self.assertEqual(result.total, len(full))
        self.assertEqual(result.offset, 0)
        self.assertEqual(result.max_results, 25)
        self.assertFalse(result.truncated)

    def test_max_results_limits_the_number_of_results(self):
        """`max_results` must cap the number of returned rules."""
        result = rules_search("valve", max_results=1)
        self.assertEqual(len(result.results), 1)

    def test_max_results_reached_before_end_reports_truncated(self):
        """When more matches exist beyond the page, `truncated` must be True."""
        full = server._get_rules().search("valve")  # pylint: disable=protected-access
        self.assertGreater(len(full), 1)
        result = rules_search("valve", max_results=1)
        self.assertEqual(result.total, len(full))
        self.assertTrue(result.truncated)

    def test_max_results_covering_all_matches_reports_not_truncated(self):
        """When the page covers every match, `truncated` must be False even at the cap."""
        full = server._get_rules().search("valve")  # pylint: disable=protected-access
        result = rules_search("valve", max_results=len(full))
        self.assertEqual(len(result.results), len(full))
        self.assertFalse(result.truncated)

    def test_offset_skips_leading_results(self):
        """`offset` must skip the given number of leading matches."""
        full = server._get_rules().search("valve")  # pylint: disable=protected-access
        self.assertGreater(len(full), 1)
        result = rules_search("valve", max_results=1, offset=1)
        self.assertEqual(result.results, full[1:2])

    def test_offset_beyond_results_returns_empty_list_but_reports_total(self):
        """An `offset` past the end of the results must return an empty page, not truncated, with the true total."""
        full = server._get_rules().search("valve")  # pylint: disable=protected-access
        result = rules_search("valve", offset=10_000)
        self.assertEqual(result.results, [])
        self.assertEqual(result.total, len(full))
        self.assertFalse(result.truncated)
