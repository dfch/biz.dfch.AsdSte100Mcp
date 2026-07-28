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

"""Tests for Word Pydantic model conversion."""

import unittest

from biz.dfch.asdste100vocab import Vocab

from biz.dfch.asdste100mcp.models import Word


class TestWord(unittest.TestCase):
    """Tests for Word Pydantic model conversion."""

    def setUp(self):
        self.vocab = Vocab()

    def test_word_model_validate_from_dict(self):
        """Converting a vocab Word to a Pydantic Word model must succeed."""
        words = self.vocab.find("use")
        self.assertGreater(len(words), 0)
        word = words[0]
        result = Word.model_validate(Vocab._word_to_dict(word))  # pylint: disable=protected-access
        self.assertIsInstance(result, Word)
        self.assertIsInstance(result.name, str)
        self.assertGreater(len(result.name), 0)

    def test_word_model_has_status(self):
        """A converted Word model must have a non-empty status field."""
        words = self.vocab.find("use")
        word = words[0]
        result = Word.model_validate(Vocab._word_to_dict(word))  # pylint: disable=protected-access
        self.assertIsInstance(result.status, str)
        self.assertGreater(len(result.status), 0)
