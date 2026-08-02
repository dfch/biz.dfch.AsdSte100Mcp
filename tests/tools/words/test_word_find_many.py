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

"""Tests for the word_find_many tool."""

import unittest

from biz.dfch.asdste100mcp import server
from biz.dfch.asdste100mcp.models import Word, WordFindEntry
from biz.dfch.asdste100mcp.tools.words.word_find_many import word_find_many
from biz.dfch.asdste100vocab import Vocab


class TestWordFindManyTool(unittest.TestCase):
    """Tests for the `word_find_many` MCP tool function."""

    def setUp(self):
        server._vocab = Vocab()  # pylint: disable=protected-access

    def tearDown(self):
        server._vocab = None  # pylint: disable=protected-access

    def test_returns_one_entry_per_input_term_in_order(self):
        """The result must have exactly one entry per input term, in the same order."""
        result = word_find_many(["use", "zzznonsense"])
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        for entry in result:
            self.assertIsInstance(entry, WordFindEntry)
        self.assertEqual(result[0].term, "use")
        self.assertEqual(result[1].term, "zzznonsense")

    def test_known_word_entry_has_results(self):
        """A known STE100 word must produce an entry with at least one result."""
        result = word_find_many(["use"])
        self.assertGreater(len(result[0].results), 0)
        for item in result[0].results:
            self.assertIsInstance(item, Word)

    def test_unknown_word_entry_has_empty_results(self):
        """An unknown word must produce an entry with an empty results list, not a missing entry."""
        result = word_find_many(["zzznonsense"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].term, "zzznonsense")
        self.assertEqual(result[0].results, [])

    def test_entry_matches_underlying_word_find_call(self):
        """Each entry's results must match what `word_find` would return for that term alone."""
        from biz.dfch.asdste100mcp.tools.words.word_find import word_find  # pylint: disable=import-outside-toplevel

        expected = word_find("use")
        result = word_find_many(["use"])
        self.assertEqual([w.name for w in expected], [w.name for w in result[0].results])

    def test_mixed_known_and_unknown_terms(self):
        """A mix of known and unknown terms must each get their own correctly populated entry."""
        result = word_find_many(["use", "zzznonsense", "use"])
        self.assertEqual(len(result), 3)
        self.assertGreater(len(result[0].results), 0)
        self.assertEqual(result[1].results, [])
        self.assertGreater(len(result[2].results), 0)


if __name__ == "__main__":
    unittest.main()
