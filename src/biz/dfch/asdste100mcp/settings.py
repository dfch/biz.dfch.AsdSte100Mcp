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

"""Typed configuration via pydantic-settings.

All settings are read from environment variables with the ``STE100_MCP_``
prefix.  A ``.env`` file is loaded by the CLI before the server starts, so
values set there are visible here.

Environment variables
---------------------
STE100_MCP_FILES
    Colon-separated list of paths to additional vocabulary files to load.
    Example: ``STE100_MCP_FILES=/data/custom.jsonl:/data/extra.jsonl``
STE100_MCP_USE_STE100
    Load the built-in ASD-STE100 Issue 9 vocabulary (default: true).
STE100_MCP_USE_STE100_TECHNICAL_WORDS
    Also load the STE100 technical words vocabulary (default: false).
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Vocab initialisation settings."""

    model_config = SettingsConfigDict(env_prefix="STE100_MCP_", extra="ignore")

    files: list[Path] = Field(default_factory=list)
    use_ste100: bool = True
    use_ste100_technical_words: bool = False
