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

"""Tests for the rules_examples tool."""

import unittest

from biz.dfch.asdste100mcp import server
from biz.dfch.asdste100mcp.tools.rules.rules_examples import rules_examples
from biz.dfch.asdste100rules.models import ContentType
from biz.dfch.asdste100rules.rules import Rules


class TestRulesExamples(unittest.TestCase):
    """Tests for the rules_examples tool."""

    def setUp(self):
        self.rules = Rules()

    def test_examples_without_filters_returns_all_content_items(self):
        """Calling examples() with no filters must return every content item."""
        result = self.rules.examples()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_examples_filtered_by_id_returns_only_that_rule(self):
        """Filtering by id must only return content items of that rule."""
        result = self.rules.examples(id_="GR-1")
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertEqual(item.rule_id, "GR-1")

    def test_examples_filtered_by_kind_returns_only_that_type(self):
        """Filtering by kind must only return content items of that type."""
        result = self.rules.examples(kind=ContentType.STE_EXAMPLE)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertEqual(item.type_, ContentType.STE_EXAMPLE)

    def test_examples_unknown_id_returns_empty_list(self):
        """Filtering by an id that does not exist must return an empty list."""
        result = self.rules.examples(id_="zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class TestRulesExamplesToolPagination(unittest.TestCase):
    """Tests for the `max_results`/`offset` pagination of the rules_examples tool."""

    def setUp(self):
        server._rules = Rules()  # pylint: disable=protected-access

    def tearDown(self):
        server._rules = None  # pylint: disable=protected-access

    def test_default_max_results_matches_unpaginated_examples(self):
        """With no pagination arguments, the tool must return the first page (up to the default cap)."""
        full = server._get_rules().examples(id_="GR-1")  # pylint: disable=protected-access
        result = rules_examples(id_="GR-1")
        self.assertEqual(result.results, full[:25])
        self.assertEqual(result.total, len(full))
        self.assertEqual(result.offset, 0)
        self.assertEqual(result.max_results, 25)
        self.assertFalse(result.truncated)

    def test_max_results_limits_the_number_of_results(self):
        """`max_results` must cap the number of returned content items."""
        result = rules_examples(max_results=1)
        self.assertEqual(len(result.results), 1)

    def test_max_results_reached_before_end_reports_truncated(self):
        """When more content items exist beyond the page, `truncated` must be True."""
        full = server._get_rules().examples()  # pylint: disable=protected-access
        self.assertGreater(len(full), 1)
        result = rules_examples(max_results=1)
        self.assertEqual(result.total, len(full))
        self.assertTrue(result.truncated)

    def test_max_results_covering_all_matches_reports_not_truncated(self):
        """When the page covers every content item, `truncated` must be False even at the cap."""
        full = server._get_rules().examples(id_="GR-1")  # pylint: disable=protected-access
        result = rules_examples(id_="GR-1", max_results=len(full))
        self.assertEqual(len(result.results), len(full))
        self.assertFalse(result.truncated)

    def test_offset_skips_leading_results(self):
        """`offset` must skip the given number of leading content items."""
        full = server._get_rules().examples(id_="GR-1")  # pylint: disable=protected-access
        self.assertGreater(len(full), 1)
        result = rules_examples(id_="GR-1", max_results=1, offset=1)
        self.assertEqual(result.results, full[1:2])

    def test_offset_beyond_results_returns_empty_list_but_reports_total(self):
        """An `offset` past the end of the results must return an empty page, not truncated, with the true total."""
        full = server._get_rules().examples()  # pylint: disable=protected-access
        result = rules_examples(offset=10_000)
        self.assertEqual(result.results, [])
        self.assertEqual(result.total, len(full))
        self.assertFalse(result.truncated)
