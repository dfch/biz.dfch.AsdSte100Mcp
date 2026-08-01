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

"""Shared ``Annotated`` parameter definitions for the rules tools."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from biz.dfch.asdste100rules.models import ContentType, EntryType

# ---------------------------------------------------------------------------
# Required parameters
# ---------------------------------------------------------------------------

RuleId = Annotated[
    str,
    Field(
        min_length=1,
        max_length=200,
        description="The exact rule/recommendation id to search for, e.g. 'R1.1' or 'GR-8' (case-insensitive).",
    ),
]

RulePattern = Annotated[
    str,
    Field(
        min_length=1,
        max_length=200,
        description="A regular-expression pattern matched against the rule name and summary (case-insensitive).",
    ),
]

SearchPattern = Annotated[
    str,
    Field(
        min_length=1,
        max_length=200,
        description=(
            "A regular-expression pattern (case-insensitive) matched against the rule section, category, "
            "name, summary, and every content block (text, notes, examples, technical noun/verb lists, ...)."
        ),
    ),
]

Section = Annotated[
    str,
    Field(min_length=1, max_length=200, description="The exact section name to search for, e.g. 'Words'."),
]

Category = Annotated[
    str,
    Field(
        min_length=1,
        max_length=200,
        description="The exact category name to search for, e.g. 'Technical nouns'.",
    ),
]

# ---------------------------------------------------------------------------
# Optional filter parameters
# ---------------------------------------------------------------------------

OptionalId = Annotated[
    str | None,
    Field(default=None, description="Only consider the rule with this exact id (case-insensitive)."),
]

OptionalSection = Annotated[
    str | None,
    Field(default=None, description="Only consider rules in this exact section (case-insensitive)."),
]

OptionalCategory = Annotated[
    str | None,
    Field(default=None, description="Only consider rules in this exact category (case-insensitive)."),
]

Kind = Annotated[
    ContentType | None,
    Field(default=None, description="Only return content items of this exact type, e.g. 'ste_example'."),
]

ContentTypes = Annotated[
    list[ContentType] | None,
    Field(
        default=None,
        description=(
            "Only search the content of these types, e.g. ['note', 'ste_example']. "
            "The rule section/category/name/summary are always searched regardless of this option."
        ),
    ),
]

Brief = Annotated[
    bool,
    Field(default=True, description="When true (default), omit the summary to keep the payload small."),
]

EntryTypeParam = Annotated[
    EntryType | None,
    Field(
        default=None,
        description=(
            "Only consider entries of this exact type, e.g. 'rule' (excludes recommendations and information blocks)."
        ),
    ),
]
