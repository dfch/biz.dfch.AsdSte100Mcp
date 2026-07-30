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

"""Tests for the find tool."""

import unittest

from biz.dfch.asdste100vocab import Vocab


class TestFind(unittest.TestCase):
    """Tests for the find tool."""

    def setUp(self):
        self.vocab = Vocab()

    def test_find_known_word_returns_results(self):
        """Finding a known STE100 word must return at least one entry."""
        result = self.vocab.find("use")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_find_unknown_word_returns_empty_list(self):
        """Finding a word that does not exist must return an empty list."""
        result = self.vocab.find("zzznonsense")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
