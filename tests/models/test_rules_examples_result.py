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

"""Tests for the RulesExamplesResult Pydantic model."""

import unittest

from biz.dfch.asdste100mcp.models import RulesExamplesResult


class TestRulesExamplesResult(unittest.TestCase):
    """Tests for the RulesExamplesResult Pydantic model."""

    def test_rules_examples_result_holds_fields(self):
        """A RulesExamplesResult must store all given fields as-is."""
        result = RulesExamplesResult(results=[], total=3, offset=0, max_results=1, truncated=True)
        self.assertEqual(result.results, [])
        self.assertEqual(result.total, 3)
        self.assertEqual(result.offset, 0)
        self.assertEqual(result.max_results, 1)
        self.assertTrue(result.truncated)

    def test_rules_examples_result_results_default_to_empty_list(self):
        """Omitting results must default to an empty list."""
        result = RulesExamplesResult(total=0, offset=0, max_results=25, truncated=False)
        self.assertEqual(result.results, [])
