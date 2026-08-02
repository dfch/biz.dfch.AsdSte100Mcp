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

"""Tests for the word_synonym tool."""

import unittest

from biz.dfch.asdste100mcp import server
from biz.dfch.asdste100mcp.models import Word
from biz.dfch.asdste100mcp.tools.words.word_synonym import word_synonym
from biz.dfch.asdste100nlp import Nlp
from biz.dfch.asdste100vocab import Vocab


class TestWordSynonym(unittest.TestCase):
    """Tests for the `Nlp.synonym` lookup backing the word_synonym tool."""

    def setUp(self):
        self.vocab = Vocab()
        self.nlp = Nlp(self.vocab)

    def test_synonym_known_word_returns_results(self):
        """A synonym lookup for a known word must return at least one entry."""
        result = self.nlp.synonym("quick")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_synonym_finds_expected_alternative(self):
        """The synonym lookup for 'quick' must include the vocabulary entry 'fast'."""
        result = self.nlp.synonym("quick")
        names = [item.name.lower() for item in result]
        self.assertIn("fast", names)

    def test_synonym_excludes_the_word_itself(self):
        """The word searched for must never appear in its own synonym results."""
        result = self.nlp.synonym("quick")
        names = [item.name.lower() for item in result]
        self.assertNotIn("quick", names)

    def test_synonym_out_of_vocabulary_word_returns_empty_list(self):
        """A synonym lookup for a nonsense word must return an empty list."""
        result = self.nlp.synonym("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class TestWordSynonymTool(unittest.TestCase):
    """Tests for the `word_synonym` MCP tool function itself."""

    def setUp(self):
        server._vocab = Vocab()  # pylint: disable=protected-access
        server._nlp = Nlp(server._vocab)  # pylint: disable=protected-access

    def tearDown(self):
        server._vocab = None  # pylint: disable=protected-access
        server._nlp = None  # pylint: disable=protected-access

    def test_tool_returns_list_of_words(self):
        """The tool must return a list of `Word` models for a known word."""
        result = word_synonym("quick")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertIsInstance(item, Word)

    def test_tool_matches_underlying_nlp_synonym_call(self):
        """The tool's results must match a direct call to `Nlp.synonym`."""
        expected = server._get_nlp().synonym("quick")  # pylint: disable=protected-access
        result = word_synonym("quick")
        self.assertEqual([w.name for w in expected], [w.name for w in result])

    def test_tool_unknown_word_returns_empty_list(self):
        """The tool must return an empty list for an out-of-vocabulary word."""
        result = word_synonym("zzznonsense")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
