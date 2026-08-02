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

"""Tests for the VersionInfo Pydantic model."""

import unittest

from biz.dfch.asdste100mcp.models import VersionInfo


class TestVersionInfo(unittest.TestCase):
    """Tests for the VersionInfo Pydantic model."""

    def test_version_info_holds_fields(self):
        """A VersionInfo must store mcp, vocab, rules, and nlp as given."""
        info = VersionInfo(mcp="1.0.0", vocab="2.0.0", rules="3.0.0", nlp="4.0.0")
        self.assertEqual(info.mcp, "1.0.0")
        self.assertEqual(info.vocab, "2.0.0")
        self.assertEqual(info.rules, "3.0.0")
        self.assertEqual(info.nlp, "4.0.0")
