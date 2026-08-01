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

"""Tests for the rules_search tool."""

import unittest

from biz.dfch.asdste100rules.models import ContentType
from biz.dfch.asdste100rules.rules import Rules


class TestRulesSearch(unittest.TestCase):
    """Tests for the rules_search tool."""

    def setUp(self):
        self.rules = Rules()

    def test_search_known_pattern_returns_results(self):
        """Full-text search for a word found only in content blocks must return entries."""
        result = self.rules.search("valve")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_search_unknown_pattern_returns_empty_list(self):
        """Full-text search for a pattern that appears nowhere must return an empty list."""
        result = self.rules.search("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_search_with_content_types_filters_results(self):
        """Restricting to a content type must not return more than the unrestricted search."""
        unrestricted = self.rules.search("valve")
        restricted = self.rules.search("valve", content_types=[ContentType.STE_EXAMPLE])
        self.assertLessEqual(len(restricted), len(unrestricted))
