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

"""Tests for the TocEntry Pydantic model."""

import unittest

from biz.dfch.asdste100mcp.models import TocEntry


class TestTocEntry(unittest.TestCase):
    """Tests for the TocEntry Pydantic model."""

    def test_toc_entry_holds_fields(self):
        """A TocEntry must store section, category, and ids as given."""
        entry = TocEntry(section="Words", category="Part of speech", ids=["R1.1", "R1.2"])
        self.assertEqual(entry.section, "Words")
        self.assertEqual(entry.category, "Part of speech")
        self.assertEqual(entry.ids, ["R1.1", "R1.2"])

    def test_toc_entry_ids_default_to_empty_list(self):
        """Omitting ids must default to an empty list."""
        entry = TocEntry(section="Words", category="Part of speech")
        self.assertEqual(entry.ids, [])
