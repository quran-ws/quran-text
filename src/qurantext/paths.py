"""Every directory the build reads or writes, anchored to the repository root.

These used to be relative to the working directory, so the build was correct
only when it was started from the root: run from anywhere else it read no
packages and wrote its output into whatever directory it happened to be in,
without complaining.  Anchoring them to this file's own location means the
build does the same thing from wherever it is invoked.
"""

from __future__ import annotations

from pathlib import Path

#: This file is ``<root>/src/qurantext/paths.py``.
ROOT = Path(__file__).resolve().parents[2]

#: The KFGQPC packages and the hand-recorded evidence beside them.
DATA = ROOT / "data"

#: The published dataset.  Committed, and rewritten in full by every build.
OUT = ROOT / "out"

#: The schemas the published files are checked against.
SCHEMA = ROOT / "schema"

#: Scratch.  Nothing here is committed and nothing reads it but the build.
WORK = ROOT / "work"
