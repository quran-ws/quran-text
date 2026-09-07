# Before this repository goes public

The repository is private, has no tags and no releases. This is what stands
between it and a first public version. Tick items off here rather than in a
conversation, so the list survives.

## Done

- [x] moved to `quran-ws/quran-text`, package identity moved with it
- [x] **CC BY 4.0** over everything, including the six client libraries, which
      each bundle the dataset (`LICENSE`, `NOTICE.md`)
- [x] every name audited against the Quran.ws terminology standard — 0 findings,
      251 external names quoted rather than renamed (`.terminology.json`)
- [x] **CI** runs the build, the tests, the client library on the Python version
      it claims, and the terminology audit (`.github/workflows/ci.yml`)
- [x] `build.py` exits non-zero when its checks find anything, so CI and any
      caller chaining on `&&` can act on it
- [x] schema `$id`s resolve — they pointed at a GitHub path that would have 404ed
- [x] no edition has an unexplained āyah end; `open-findings.json` is empty
- [x] `ln` is exact for Ḥafṣ and Shuʿbah (6,236 / 6,236)

## Blocking

- [ ] **Confirm KFGQPC's redistribution terms.** `NOTICE.md` tells others to
      satisfy themselves; going public distributes 17 packages and 7 fonts, so
      that advice should rest on something confirmed rather than inferred. The
      packages state no terms in their `read.me`.
- [ ] **Set `GUIDELINES_TOKEN`** in repository secrets. `quran-ws/guidelines` is
      private, so without it the terminology job warns and passes — the audit is
      not actually enforced until the secret exists.

## Should do

- [ ] `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`
- [ ] **Tag `v1.0.0` and cut a release.** `NOTICE.md` promises whoever receives
      this data second-hand that the link reaches "corrections and later
      releases". There is nothing at the other end of that promise yet.
- [ ] **`out/word-index.json` is 48 MB**, against GitHub's 50 MB warning
      threshold, and it is rewritten on every build.
- [ ] **`service/tests/` cannot run** without pytest and fastapi in a virtualenv,
      so CI does not cover the service at all. Either wire the venv into CI or
      say in `service/README.md` that the suite needs one.
- [ ] **Two stale branches**, both predating the terminology rename and so
      needing the same merge treatment: `feat/hybrid-slot-model` (1 commit),
      `review-page` (2).
- [ ] GitHub `homepage` is empty while every package manifest points at
      `quran.ws`.

## Decisions

- [ ] **Flip to public.** Everything above is reversible while it is private;
      publication is not — the data is mirrored the moment it is out.
- [ ] **Publish the six packages** to npm, PyPI, Packagist, pub.dev and Maven
      Central? The manifests are ready and declare `CC-BY-4.0`. Registry names
      are claimed by whoever publishes first.
- [ ] **Ship with the two open questions in `verify-in-print.md`** — Bazzī's juz
      26, and the six āyahs with no `rasm_imlai` — or resolve them first. Both
      are documented rather than hidden, which is what a known-issues file is for.
- [ ] **The 240 `rubu_al_hizb` positions exist only as prose in
      `known-issues.md` §7.** There are no `hizb_starts` or `rubu_al_hizb_starts`
      layers, and the thirteen medallion readings behind them are not recorded
      anywhere machine-readable, so that work would have to be redone from the
      printed muṣḥaf if the layers are wanted later.
