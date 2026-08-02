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

"""Tests for the Settings.Factory singleton."""

import unittest
from pathlib import Path

from biz.dfch.asdste100mcp.settings import Factory, Settings


class TestFactory(unittest.TestCase):
    """Tests for Factory.create_instance and Factory.get_instance."""

    def tearDown(self):
        """Reset the singleton after every test so tests do not interfere."""
        Factory._instance = None  # pylint: disable=protected-access

    # ------------------------------------------------------------------
    # create_instance
    # ------------------------------------------------------------------

    def test_create_instance_returns_settings(self):
        """create_instance() must return a Settings object."""
        result = Factory.create_instance()
        self.assertIsInstance(result, Settings)

    def test_create_instance_without_extra_files_returns_settings(self):
        """create_instance() called with no arguments must succeed."""
        result = Factory.create_instance()
        self.assertIsInstance(result, Settings)
        self.assertIsInstance(result.vocab_files, list)

    def test_create_instance_with_extra_files_merges_paths(self):
        """Extra files passed to create_instance() must appear in settings.files."""
        extra = [Path("/tmp/opencode/a.jsonl"), Path("/tmp/opencode/b.jsonl")]
        result = Factory.create_instance(extra_files=extra)
        for path in extra:
            self.assertIn(path, result.vocab_files)

    def test_create_instance_deduplicates_extra_files(self):
        """Duplicate paths must appear only once in settings.files."""
        path = Path("/tmp/opencode/a.jsonl")
        result = Factory.create_instance(extra_files=[path, path])
        self.assertEqual(result.vocab_files.count(path), 1)

    def test_create_instance_without_extra_rules_files_returns_settings(self):
        """create_instance() called with no rules args must succeed."""
        result = Factory.create_instance()
        self.assertIsInstance(result, Settings)
        self.assertIsInstance(result.rules_files, list)

    def test_create_instance_with_extra_rules_files_merges_paths(self):
        """Extra rules files passed to create_instance() must appear in settings.rules_files."""
        extra = [Path("/tmp/opencode/a.json"), Path("/tmp/opencode/b.json")]
        result = Factory.create_instance(extra_rules_files=extra)
        for path in extra:
            self.assertIn(path, result.rules_files)

    def test_create_instance_deduplicates_extra_rules_files(self):
        """Duplicate rules file paths must appear only once in settings.rules_files."""
        path = Path("/tmp/opencode/a.json")
        result = Factory.create_instance(extra_rules_files=[path, path])
        self.assertEqual(result.rules_files.count(path), 1)

    def test_create_instance_twice_raises(self):
        """Calling create_instance() a second time must raise AssertionError."""
        Factory.create_instance()
        with self.assertRaises(AssertionError):
            Factory.create_instance()

    # ------------------------------------------------------------------
    # get_instance
    # ------------------------------------------------------------------

    def test_get_instance_before_create_raises(self):
        """get_instance() before create_instance() must raise AssertionError."""
        with self.assertRaises(AssertionError):
            Factory.get_instance()

    def test_get_instance_returns_same_object(self):
        """get_instance() must return the exact object created by create_instance()."""
        created = Factory.create_instance()
        retrieved = Factory.get_instance()
        self.assertIs(created, retrieved)

    def test_get_instance_called_multiple_times_returns_same_object(self):
        """Repeated calls to get_instance() must return the same object."""
        Factory.create_instance()
        first = Factory.get_instance()
        second = Factory.get_instance()
        self.assertIs(first, second)
