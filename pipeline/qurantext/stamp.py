"""The one date the build stamps into what it publishes.

Every published file carries a ``generated`` date — the seven muṣḥaf files, the
word index, the āyah map, the counting file, the catalogue, the viewer and the
manifest — and ``data/COMPARISON.md`` opens by naming the same day.  It used to
be ``date.today()``, read afresh at each of the nine sites.

That made the build unreproducible.  ``.github/workflows/ci.yml`` takes as its
premise that the build reads only what is committed, so that a fresh clone must
reproduce ``data/`` exactly; a date drawn from the clock breaks the premise on
the first day nobody rebuilds.  Worse, ``manifest.json`` records a SHA-256 for
every file, so a date that moved when no input had moved churned every checksum
under it.  A checksum that changes when nothing changed tells a reader nothing —
the same defect the gzip timestamps had, one layer up.

Dropping the date would fix reproducibility and lose something real: ``generated``
is required by all four schemas, and a dataset that cannot say which edition a
file belongs to is harder to cite.  So the date stays, and stops coming from the
clock.  It is a fact this repository declares and commits, like the source
hashes beside it, and two builds a year apart from the same commit agree on it.

``SOURCE_DATE_EPOCH`` is the reproducible-builds convention for exactly this: a
distributor exports it, and every timestamp a build would otherwise take from
the clock is taken from it instead.  Honouring it lets a release pipeline stamp
its own date without patching source, and lets anyone re-derive a published file
byte for byte by exporting the date that file already carries.  Unset — the
ordinary case, and the case CI runs in — the build uses :data:`EDITION` below.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

#: The edition date of the dataset committed under ``data/``.
#:
#: Bump it when publishing a build whose inputs changed, in the same commit that
#: carries the rebuilt files; leave it alone when rebuilding unchanged inputs,
#: which is what keeps the rebuild byte-identical.  It cannot be derived from
#: git: the commit that changes ``sources/`` is also the commit that carries the
#: rebuilt ``data/``, so a date read from the log would be one commit behind
#: whatever it described, and CI — rebuilding after that commit exists — would
#: compute a different one and report a tree that never matches.
EDITION = "2026-09-08"


def generated() -> str:
    """The ``generated`` date every published file carries, as ``YYYY-MM-DD``."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if not epoch:
        return EDITION
    try:
        seconds = int(epoch)
    except ValueError:
        raise SystemExit(
            f"SOURCE_DATE_EPOCH must be whole seconds since the Unix epoch; got {epoch!r}."
        ) from None
    # UTC, not local time: the same epoch must name the same day everywhere, or
    # two machines in different zones would stamp different dates from it.
    return datetime.fromtimestamp(seconds, timezone.utc).date().isoformat()
