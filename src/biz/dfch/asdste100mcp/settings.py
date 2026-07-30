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

Singleton helpers
-----------------
Factory.create_instance(extra_files)
    Create the shared :class:`Settings` instance from the environment,
    merge *extra_files* (e.g. from the ``--file`` CLI flag), and store it.
    Must be called exactly once before :meth:`Factory.get_instance`.
Factory.get_instance()
    Return the shared :class:`Settings` instance.  Raises
    :exc:`AssertionError` if :meth:`Factory.create_instance` has not been
    called yet.
"""

import threading
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# ---------------------------------------------------------------------------
# Settings model
# ---------------------------------------------------------------------------


class Settings(BaseSettings):
    """Vocab initialisation settings."""

    model_config = SettingsConfigDict(env_prefix="STE100_MCP_", extra="ignore")

    files: list[Path] = Field(default_factory=list)
    use_ste100: bool = True
    use_ste100_technical_words: bool = False


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


class Factory:
    """Thread-safe singleton factory for :class:`Settings`.

    Class-level state removes the need for a module-level ``global``
    variable.  Use a double-checked lock so that concurrent first-callers
    do not race to create duplicate instances.

    Typical call sequence
    ---------------------
    1. CLI calls :meth:`create_instance` (once, before ``mcp.run()``).
    2. Server lifespan calls :meth:`get_instance` (one or more times).
    """

    _instance: Settings | None = None
    _lock: threading.Lock = threading.Lock()

    @staticmethod
    def create_instance(extra_files: list[Path] | None = None) -> Settings:
        """Create and store the shared :class:`Settings` instance.

        Reads configuration from environment variables, merges *extra_files*
        with any paths already set via ``STE100_MCP_FILES`` (duplicates
        removed, order preserved), and stores the result.

        Parameters
        ----------
        extra_files:
            Additional vocabulary file paths from the CLI ``--file`` flag.

        Returns
        -------
        Settings
            The newly created singleton instance.

        Raises
        ------
        AssertionError
            If the singleton has already been created.
        """
        assert Factory._instance is None, (
            "Settings instance already created — create_instance() must be called only once."
        )

        with Factory._lock:
            if Factory._instance is None:
                settings = Settings()
                merged = list(dict.fromkeys(settings.files + (extra_files or [])))
                settings.files = merged
                Factory._instance = settings

        return Factory._instance

    @staticmethod
    def get_instance() -> Settings:
        """Return the shared :class:`Settings` instance.

        Returns
        -------
        Settings
            The singleton settings instance.

        Raises
        ------
        AssertionError
            If :meth:`create_instance` has not been called yet.
        """
        assert Factory._instance is not None, "Settings not initialised — call create_instance() before get_instance()."
        return Factory._instance
