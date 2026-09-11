"""The search fold conformance vector — the same file every quran-ws
implementation is tested against.  See docs/SEARCH-FOLD.md."""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib" / "python"))
import quran_text as qt  # noqa: E402

VECTORS = json.loads(
    (pathlib.Path(__file__).with_name("search-fold.json")).read_text(encoding="utf8")
)["vectors"]


@pytest.mark.parametrize("case", VECTORS, ids=[c["note"][:48] for c in VECTORS])
def test_vector(case):
    assert qt.search_key(case["input"]) == case["search_key"]
    assert qt.match_fold(case["input"]) == case["match_fold"]
    assert qt.loose_key(case["input"]) == case["loose_key"]


def test_the_bug_this_replaces():
    """Both spellings of the query reach the same ayat.

    `fold()` used to expand the dagger alif into a full alif, so the spelling a
    phone keyboard produces returned nothing at all.
    """
    m = qt.Mushaf.hafs()
    strict = m.search("الرحمن")
    assert len(strict) == 45
    assert not any(s.loose for s in strict)

    fallback = m.search("الرحمان")
    assert len(fallback) == 45
    assert all(s.loose for s in fallback), "the second spelling is a loose match"


def test_hamza_forms_are_folded_both_ways():
    m = qt.Mushaf.hafs()
    assert len(m.search("انعمت")) == len(m.search("أنعمت")) == 7


def test_dagger_alif_is_never_expanded():
    # The uthmani writes this with a dagger alif; modern spelling writes a full
    # alif, and the imlai column is what knows that.
    assert qt.match_fold("ٱلۡعَٰلَمِينَ") == "العلمين"
    assert qt.match_fold("العالمين") == "العالمين"
    assert qt.Mushaf.hafs().search("العالمين")
