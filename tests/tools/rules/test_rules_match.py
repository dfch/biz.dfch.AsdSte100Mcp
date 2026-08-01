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

"""Tests for the rules_match tool."""

import unittest

from biz.dfch.asdste100rules.rules import Rules


class TestRulesMatch(unittest.TestCase):
    """Tests for the rules_match tool."""

    def setUp(self):
        self.rules = Rules()

    def test_match_known_pattern_returns_results(self):
        """Matching a common word in rule names/summaries must return entries."""
        result = self.rules.match("verb")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_match_unknown_pattern_returns_empty_list(self):
        """Matching a pattern that appears nowhere must return an empty list."""
        result = self.rules.match("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
