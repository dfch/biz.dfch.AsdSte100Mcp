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

"""Tests for the word_similar tool."""

import unittest

from biz.dfch.asdste100vocab import Vocab


class TestWordSimilar(unittest.TestCase):
    """Tests for the word_similar tool."""

    def setUp(self):
        self.vocab = Vocab()

    def test_similar_returns_results(self):
        """A fuzzy lookup for a known word must return at least one entry."""
        result = self.vocab.similar("use")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_similar_returns_list_for_unknown_word(self):
        """A fuzzy lookup for a nonsense word must return a list (possibly empty)."""
        result = self.vocab.similar("zzznonsense")
        self.assertIsInstance(result, list)
