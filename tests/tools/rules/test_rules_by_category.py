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

"""Tests for the rules_by_category tool."""

import unittest

from biz.dfch.asdste100rules.rules import Rules


class TestRulesByCategory(unittest.TestCase):
    """Tests for the rules_by_category tool."""

    def setUp(self):
        self.rules = Rules()

    def test_by_category_known_category_returns_results(self):
        """Searching a known category must return at least one entry."""
        result = self.rules.by_category("General recommendations")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for rule in result:
            self.assertEqual(rule.category, "General recommendations")

    def test_by_category_is_case_insensitive(self):
        """Searching a known category in a different case must still match."""
        result = self.rules.by_category("general recommendations")
        self.assertGreater(len(result), 0)

    def test_by_category_unknown_category_returns_empty_list(self):
        """Searching a category that does not exist must return an empty list."""
        result = self.rules.by_category("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
