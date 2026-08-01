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

"""Tests for the rules_find tool."""

import unittest

from biz.dfch.asdste100rules.rules import Rules


class TestRulesFind(unittest.TestCase):
    """Tests for the rules_find tool."""

    def setUp(self):
        self.rules = Rules()

    def test_find_known_id_returns_results(self):
        """Finding a known rule id must return exactly one entry."""
        result = self.rules.find("R1.1")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id_, "R1.1")

    def test_find_is_case_insensitive(self):
        """Finding a known rule id in a different case must still match."""
        result = self.rules.find("r1.1")
        self.assertEqual(len(result), 1)

    def test_find_unknown_id_returns_empty_list(self):
        """Finding an id that does not exist must return an empty list."""
        result = self.rules.find("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
