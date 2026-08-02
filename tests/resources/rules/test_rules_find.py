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

"""Tests for the asdste100://rules/rule/{id_} resource template."""

import unittest

from biz.dfch.asdste100mcp import server
from biz.dfch.asdste100mcp.resources.rules.rules_find import rules_find
from biz.dfch.asdste100rules.rules import Rules


class TestRulesFindResource(unittest.TestCase):
    """Tests for the `rules_find` resource function (`asdste100://rules/rule/{id_}`)."""

    def setUp(self):
        server._rules = Rules()  # pylint: disable=protected-access

    def tearDown(self):
        server._rules = None  # pylint: disable=protected-access

    def test_known_id_returns_exactly_one_rule(self):
        """Looking up a known rule id must return exactly one entry."""
        result = rules_find("R1.1")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id_, "R1.1")

    def test_is_case_insensitive(self):
        """Looking up a known rule id in a different case must still match."""
        result = rules_find("r1.1")
        self.assertEqual(len(result), 1)

    def test_unknown_id_returns_empty_list(self):
        """Looking up an id that does not exist must return an empty list, not raise."""
        result = rules_find("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_matches_underlying_rules_find(self):
        """The resource must mirror `Rules.find()` exactly."""
        expected = server._get_rules().find("R1.1")  # pylint: disable=protected-access
        result = rules_find("R1.1")
        self.assertEqual(result, expected)
