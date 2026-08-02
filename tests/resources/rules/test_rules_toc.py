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

"""Tests for the asdste100://rules/toc resource."""

import unittest

from biz.dfch.asdste100mcp import server
from biz.dfch.asdste100mcp.models import TocEntry
from biz.dfch.asdste100mcp.resources.rules.rules_toc import rules_toc
from biz.dfch.asdste100rules.rules import Rules


class TestRulesTocResource(unittest.TestCase):
    """Tests for the `rules_toc` resource function (`asdste100://rules/toc`)."""

    def setUp(self):
        server._rules = Rules()  # pylint: disable=protected-access

    def tearDown(self):
        server._rules = None  # pylint: disable=protected-access

    def test_returns_toc_entry_list(self):
        """The resource must return a list of `TocEntry` instances."""
        result = rules_toc()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for entry in result:
            self.assertIsInstance(entry, TocEntry)

    def test_matches_underlying_rules_toc(self):
        """The resource must mirror `Rules.toc()` with no filter, converted to `TocEntry`."""
        pairs = server._get_rules().toc()  # pylint: disable=protected-access
        result = rules_toc()
        self.assertEqual(len(result), len(pairs))
        for entry, (section, category, ids) in zip(result, pairs):
            self.assertEqual(entry.section, section)
            self.assertEqual(entry.category, category)
            self.assertEqual(entry.ids, ids)
