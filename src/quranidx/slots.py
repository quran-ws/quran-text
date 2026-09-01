"""Publish the explicit slot/token/position model and its review report."""

from __future__ import annotations

import json
from collections import Counter
from datetime import date

from .build import AlignmentSpan, ORDER, OUT, Word


def _reading(words: list[Word], key: str) -> dict:
    tokens = [{
        "slot_id": w.id,
        "legacy_word_id": w.id,
        "position": w.position[key],
        "ayah": w.aya[key],
        "text": w.forms[key],
    } for w in words if key in w.forms]
    return {
        "ayahs": list(dict.fromkeys(t["ayah"] for t in tokens)),
        "tokens": tokens,
    }


def _token_summary(w: Word, key: str) -> dict:
    return {
        "slot_id": w.id,
        "position": w.position[key],
        "ayah": w.aya[key],
        "text": w.forms[key],
    }


def slot_model(words: list[Word], spans: list[AlignmentSpan]) -> dict:
    """The machine-readable migration and exceptional-alignment inventory."""
    positions = {}
    for key in ORDER:
        values = [w.position[key] for w in words if key in w.position]
        positions[key] = {
            "word_count": len(values),
            "empty_slot_count": len(words) - len(values),
            "first": values[0] if values else None,
            "last": values[-1] if values else None,
            "contiguous": values == list(range(1, len(values) + 1)),
        }

    partial = []
    for word_index, w in enumerate(words):
        if w.status != "partial":
            continue
        neighborhood = {}
        for key in ORDER:
            before = next((candidate for candidate in reversed(words[:word_index])
                           if key in candidate.position), None)
            after = next((candidate for candidate in words[word_index + 1:]
                          if key in candidate.position), None)
            neighborhood[key] = {
                "before": _token_summary(before, key) if before else None,
                "at": _token_summary(w, key) if key in w.position else None,
                "after": _token_summary(after, key) if after else None,
            }
        partial.append({
            "slot_id": w.id,
            "legacy_word_id": w.id,
            "key": w.key,
            "sura": w.sura,
            "present": w.present,
            "missing": w.missing,
            "readings": {
                key: {
                    "ayah": w.aya[key],
                    "position": w.position[key],
                    "text": w.forms[key],
                }
                for key in w.present
            },
            "neighborhood": neighborhood,
        })

    by_id = {w.id: w for w in words}
    alignment = []
    for span in spans:
        mine = [by_id[i] for i in range(span.first_slot, span.last_slot + 1)]
        readings = {key: _reading(mine, key) for key in ORDER}
        counts = Counter(len(r["tokens"]) for r in readings.values())
        alignment.append({
            "id": span.id,
            "kind": "n_to_m",
            "sura": span.sura,
            "slots": [span.first_slot, span.last_slot],
            "slot_ids": list(range(span.first_slot, span.last_slot + 1)),
            "legacy_word_ids": list(range(span.first_slot, span.last_slot + 1)),
            "token_count_distribution": {str(n): count
                                         for n, count in sorted(counts.items())},
            "readings": readings,
        })

    return {
        "format": "quran-slot-model",
        "schema_version": "1.0",
        "generated": date.today().isoformat(),
        "model": (
            "slot_id is the shared cross-riwayah coordinate; position is the "
            "dense word ordinal inside one riwayah; an alignment span groups "
            "the rare contiguous slots whose readings do not align 1:1."
        ),
        "slot_count": len(words),
        "slot_id_range": [words[0].id, words[-1].id] if words else [],
        "slot_ids_contiguous": [w.id for w in words]
                               == list(range(1, len(words) + 1)),
        "legacy_aliases": {
            "id_equals_slot_id": True,
            "w_equals_s": True,
            "word_id_equals_slot_id": True,
        },
        "positions": positions,
        "partial_slot_count": len(partial),
        "partial_slots": partial,
        "alignment_span_count": len(alignment),
        "alignment_spans": alignment,
    }


def _texts(reading: dict) -> str:
    tokens = reading["tokens"]
    return " ".join(t["text"] for t in tokens) if tokens else "—"


def slot_report(model: dict) -> str:
    """Human-readable before/after explanation generated from ``slot_model``."""
    lines = [
        "# Slot model: before and after",
        "",
        "The alignment spine is unchanged. The migration separates the shared "
        "coordinate from the dense position of a word inside one muṣḥaf.",
        "",
        "| before | after |",
        "|---|---|",
        "| `id`, `w`, `word_id` were described as a global word ID | the same integer is explicitly `slot_id` (`s` in compact muṣḥaf JSON) |",
        "| a missing word made one muṣḥaf appear to skip a word ID | the muṣḥaf skips an empty slot but its dense `position` (`p`) remains contiguous |",
        "| an unequal replacement was forced into independent word columns | an `alignment_span` groups the columns without removing atomic word addressability |",
        "",
        f"Before: **{model['slot_count']:,} legacy IDs**. After: "
        f"**{model['slot_count']:,} slot IDs** over the same range "
        f"{model['slot_id_range'][0]}–{model['slot_id_range'][1]}. "
        f"Continuity: **{'pass' if model['slot_ids_contiguous'] else 'fail'}**. "
        "All legacy identifiers remain exact aliases.",
        "",
        "## Dense positions",
        "",
        "| riwāyah | words | empty slots | position range | contiguous |",
        "|---|---:|---:|---|---|",
    ]
    for key, row in model["positions"].items():
        lines.append(
            f"| `{key}` | {row['word_count']:,} | {row['empty_slot_count']:,} | "
            f"{row['first']}–{row['last']} | {'yes' if row['contiguous'] else 'no'} |"
        )

    lines.extend([
        "",
        "## Presence and absence: atomic slots",
        "",
        "These remain word-sized slots. A riwāyah that lacks the word has no token "
        "at that slot, while its next token still receives the next dense position.",
        "",
        "| slot | key | present | missing | forms with dense positions |",
        "|---:|---|---|---|---|",
    ])
    for row in model["partial_slots"]:
        forms = " · ".join(
            f"**{v['text']}** `{key}:p{v['position']}`"
            for key, v in row["readings"].items()
        )
        lines.append(
            f"| {row['slot_id']} | `{row['key']}` | {', '.join(row['present'])} | "
            f"{', '.join(row['missing'])} | {forms} |"
        )

    bazzi_min = next((row for row in model["partial_slots"]
                      if row["sura"] == 9
                      and row["readings"].get("bazzi", {}).get("ayah") == 101),
                     None)
    if bazzi_min:
        b = bazzi_min["neighborhood"]["bazzi"]
        h = bazzi_min["neighborhood"]["hafs"]
        lines.extend([
            "",
            "### Bazzī’s `مِن` at 9:101",
            "",
            f"Shared slot **{bazzi_min['slot_id']}** contains "
            f"**{b['at']['text']}** for Bazzī at dense position "
            f"**p{b['at']['position']}**. Bazzī’s local sequence is "
            f"p{b['before']['position']}, p{b['at']['position']}, "
            f"p{b['after']['position']}; Ḥafṣ has no token in the middle slot, "
            f"so its neighboring tokens remain consecutive at "
            f"p{h['before']['position']} and p{h['after']['position']}.",
        ])

    lines.extend([
        "",
        "## Genuine n:m alignment spans",
        "",
        "A span says that the whole token sequence corresponds; it does not claim "
        "that the first word on one side independently equals the first on the other.",
        "",
    ])
    if not model["alignment_spans"]:
        lines.append("No genuine n:m spans were detected.")
    for span in model["alignment_spans"]:
        reference = ""
        if span["sura"] == 40 and any(
                26 in reading["ayahs"] for reading in span["readings"].values()):
            reference = " (40:26 — `أَوْ أَن` / `وَأَن`)"
        lines.extend([
            f"### {span['id']} — slots {span['slots'][0]}–{span['slots'][1]}"
            f"{reference}",
            "",
            "| riwāyah | token sequence |",
            "|---|---|",
        ])
        for key, reading in span["readings"].items():
            lines.append(f"| `{key}` | {_texts(reading)} |")
        lines.append("")

    lines.extend([
        "## Compatibility",
        "",
        "Comparison schema 2.1 keeps `id` and adds `slot_id` plus a per-riwāyah "
        "`position` map. Muṣḥaf format 1.1 keeps `w`, adds its equal alias `s`, "
        "and adds dense `p`. Removing the legacy aliases requires a future major version.",
        "",
    ])
    return "\n".join(lines)


def write_slot_model(words: list[Word], spans: list[AlignmentSpan]) -> dict:
    model = slot_model(words, spans)
    (OUT / "slot-model.json").write_text(
        json.dumps(model, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "SLOT-MODEL.md").write_text(slot_report(model), encoding="utf-8")
    return model
