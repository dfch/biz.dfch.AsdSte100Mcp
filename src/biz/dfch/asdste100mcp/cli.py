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
#
# -----
# Portions of this file are derived from termdat-mcp
# (https://github.com/malkreide/termdat-mcp), specifically the dual-transport
# entry point pattern and the public-binding container detection in
# src/termdat_mcp/__main__.py.
#
# MIT License
# Copyright (c) 2026 Hayal Oezkan
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# -----

"""Typer CLI entry point for the ASD-STE100 MCP server.

The server can be started in two transport modes:

* **stdio** (default) — the host process communicates over stdin/stdout;
  suitable for OpenCode and other MCP hosts that launch the server
  as a subprocess::

      ste100-mcp
      uv run ste100-mcp
      python -m biz.dfch.asdste100mcp

* **SSE / network** — the server binds a TCP port and accepts HTTP
  connections; suitable for cloud deployments::

      ste100-mcp --transport sse --host localhost --port 8000

Environment variables (all optional, CLI flags take precedence):

``STE100_MCP_TRANSPORT``
    ``stdio`` (default) or ``sse``.
``STE100_MCP_HOST``
    Bind address for SSE mode (default ``localhost``).
``STE100_MCP_PORT``
    TCP port for SSE mode (default ``8000``).
``STE100_MCP_FILES``
    Colon-separated list of additional vocabulary files.  The ``--file``
    CLI flag is merged with this list (duplicates are removed).
``STE100_MCP_RULES_FILES``
    Colon-separated list of additional rules files.  The ``--rules-file``
    CLI flag is merged with this list (duplicates are removed).
"""

import os
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from dotenv import find_dotenv, load_dotenv

from .server import mcp
from .settings import Factory

# ---------------------------------------------------------------------------
# .env loading
# ---------------------------------------------------------------------------


def _load_default_dotenv() -> None:
    """Load ``.env`` walking upward from this file, then from CWD as fallback."""
    dotenv_path = find_dotenv(usecwd=False) or find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path, verbose=False)


_load_default_dotenv()

# ---------------------------------------------------------------------------
# Typer application
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="ste100-mcp",
    help="ASD-STE100 Issue 9 MCP server.",
    no_args_is_help=False,
    add_completion=False,
)


def _warn_on_public_binding(host: str) -> None:
    """Warn when binding to all interfaces outside a container."""
    if host not in ("0.0.0.0", "::"):
        return
    in_container = (
        os.path.exists("/.dockerenv")
        or bool(os.environ.get("KUBERNETES_SERVICE_HOST"))
        or bool(os.environ.get("RAILWAY_PROJECT_ID"))
        or bool(os.environ.get("RENDER"))
    )
    if not in_container:
        sys.stderr.write(
            f"WARNING: binding ste100-mcp to '{host}' outside a container "
            "exposes it to the local network. Use --host localhost for "
            "local development.\n"
        )


@app.command()
def serve(  # pylint: disable=R0913,R0917
    transport: Annotated[
        str,
        typer.Option(
            "--transport",
            "-t",
            envvar="STE100_MCP_TRANSPORT",
            help="Transport mode: 'stdio' or 'sse'.",
            show_default=True,
        ),
    ] = "stdio",
    host: Annotated[
        str,
        typer.Option(
            "--host",
            "-h",
            envvar="STE100_MCP_HOST",
            help="Bind address (SSE mode only).",
            show_default=True,
        ),
    ] = "localhost",
    port: Annotated[
        int,
        typer.Option(
            "--port",
            "-p",
            envvar="STE100_MCP_PORT",
            help="TCP port (SSE mode only).",
            show_default=True,
        ),
    ] = 8000,
    env_file: Annotated[
        Optional[Path],
        typer.Option(
            "--env",
            help="Path to a .env file. Overrides the auto-discovered one.",
        ),
    ] = None,
    files: Annotated[
        Optional[list[Path]],
        typer.Option(
            "--file",
            "-f",
            help="Path to a vocabulary file (*.jsonl). You can use this option more than once.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ] = None,
    rules_files: Annotated[
        Optional[list[Path]],
        typer.Option(
            "--rules-file",
            "-r",
            help="Path to a rules file (a single JSON array). You can use this option more than once.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ] = None,
) -> None:
    """Start the ASD-STE100 MCP server."""
    if env_file is not None:
        if not env_file.exists():
            typer.echo(f"ERROR: --env file not found: '{env_file}'", err=True)
            raise typer.Exit(code=1)
        load_dotenv(env_file, override=True)

    Factory.create_instance(files or [], rules_files or [])

    if transport.lower() == "sse":
        _warn_on_public_binding(host)
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    app()
