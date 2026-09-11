// The search fold conformance vector — the same file every quran-ws
// implementation is tested against. See docs/SEARCH-FOLD.md.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { Mushaf, searchKey, matchFold, looseKey } from "../lib/js/quran-text.js";

const { vectors } = JSON.parse(
  await readFile(new URL("./search-fold.json", import.meta.url), "utf8"),
);

test("conformance vector", () => {
  for (const c of vectors) {
    assert.equal(searchKey(c.input), c.search_key, `search_key: ${c.note}`);
    assert.equal(matchFold(c.input), c.match_fold, `match_fold: ${c.note}`);
    assert.equal(looseKey(c.input), c.loose_key, `loose_key: ${c.note}`);
  }
});

test("the bug this replaces: both spellings reach the same ayat", async () => {
  const m = await Mushaf.hafs();
  const strict = m.search("الرحمن");
  assert.equal(strict.length, 45);
  assert.ok(!strict.some((s) => s.loose));

  const fallback = m.search("الرحمان");
  assert.equal(fallback.length, 45);
  assert.ok(fallback.every((s) => s.loose), "the second spelling is a loose match");
});

test("hamza forms fold both ways", async () => {
  const m = await Mushaf.hafs();
  assert.equal(m.search("انعمت").length, 7);
  assert.equal(m.search("أنعمت").length, 7);
});

test("the dagger alif is never expanded", async () => {
  assert.equal(matchFold("ٱلۡعَٰلَمِينَ"), "العلمين");
  assert.equal(matchFold("العالمين"), "العالمين");
  assert.ok((await Mushaf.hafs()).search("العالمين").length);
});
