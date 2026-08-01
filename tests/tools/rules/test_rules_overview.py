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

"""Tests for the rules_overview tool."""

import unittest

from biz.dfch.asdste100rules.models import EntryType
from biz.dfch.asdste100rules.rules import Rules


class TestRulesOverview(unittest.TestCase):
    """Tests for the rules_overview tool."""

    def setUp(self):
        self.rules = Rules()

    def test_overview_without_filters_returns_one_per_rule(self):
        """Calling overview() with no filters must return one entry per rule."""
        result = self.rules.overview()
        self.assertEqual(len(result), len(self.rules))

    def test_overview_brief_omits_summary(self):
        """With brief=True (default), summary must be None."""
        result = self.rules.overview(brief=True)
        for item in result:
            self.assertIsNone(item.summary)

    def test_overview_full_includes_summary(self):
        """With brief=False, summary must be populated."""
        result = self.rules.overview(brief=False)
        self.assertTrue(all(item.summary is not None for item in result))

    def test_overview_filtered_by_type_returns_only_that_type(self):
        """Filtering by type_ must only return entries of that type."""
        result = self.rules.overview(type_=EntryType.RULE)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertEqual(item.type_, EntryType.RULE)
