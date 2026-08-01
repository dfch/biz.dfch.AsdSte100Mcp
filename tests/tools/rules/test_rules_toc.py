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

"""Tests for the rules_toc tool (and the TocEntry conversion it performs)."""

import unittest

from biz.dfch.asdste100mcp.models import TocEntry
from biz.dfch.asdste100rules.rules import Rules


class TestRulesToc(unittest.TestCase):
    """Tests for the rules_toc tool."""

    def setUp(self):
        self.rules = Rules()

    def test_toc_without_filter_returns_all_pairs(self):
        """Calling toc() with no filter must return at least one (section, category) pair."""
        result = self.rules.toc()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_toc_entries_convert_to_toc_entry_model(self):
        """Each (section, category, ids) tuple must convert into a valid TocEntry."""
        pairs = self.rules.toc()
        entries = [TocEntry(section=section, category=category, ids=ids) for section, category, ids in pairs]
        self.assertEqual(len(entries), len(pairs))
        for entry, (section, category, ids) in zip(entries, pairs):
            self.assertEqual(entry.section, section)
            self.assertEqual(entry.category, category)
            self.assertEqual(entry.ids, ids)

    def test_toc_filtered_by_section_returns_only_that_section(self):
        """Filtering by section must only return pairs for that section."""
        result = self.rules.toc(section="Words")
        self.assertGreater(len(result), 0)
        for section, _category, _ids in result:
            self.assertEqual(section, "Words")

    def test_toc_unknown_section_returns_empty_list(self):
        """Filtering by a section that does not exist must return an empty list."""
        result = self.rules.toc(section="zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
