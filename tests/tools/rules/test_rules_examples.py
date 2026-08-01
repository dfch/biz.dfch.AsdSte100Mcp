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
