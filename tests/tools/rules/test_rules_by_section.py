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

"""Tests for the rules_by_section tool."""

import unittest

from biz.dfch.asdste100rules.rules import Rules


class TestRulesBySection(unittest.TestCase):
    """Tests for the rules_by_section tool."""

    def setUp(self):
        self.rules = Rules()

    def test_by_section_known_section_returns_results(self):
        """Searching a known section must return at least one entry."""
        result = self.rules.by_section("Words")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for rule in result:
            self.assertEqual(rule.section, "Words")

    def test_by_section_is_case_insensitive(self):
        """Searching a known section in a different case must still match."""
        result = self.rules.by_section("words")
        self.assertGreater(len(result), 0)

    def test_by_section_unknown_section_returns_empty_list(self):
        """Searching a section that does not exist must return an empty list."""
        result = self.rules.by_section("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
