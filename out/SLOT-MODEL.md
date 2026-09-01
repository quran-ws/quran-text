# Slot model: before and after

The alignment spine is unchanged. The migration separates the shared coordinate from the dense position of a word inside one muṣḥaf.

| before | after |
|---|---|
| `id`, `w`, `word_id` were described as a global word ID | the same integer is explicitly `slot_id` (`s` in compact muṣḥaf JSON) |
| a missing word made one muṣḥaf appear to skip a word ID | the muṣḥaf skips an empty slot but its dense `position` (`p`) remains contiguous |
| an unequal replacement was forced into independent word columns | an `alignment_span` groups the columns without removing atomic word addressability |

Before: **77,434 legacy IDs**. After: **77,434 slot IDs** over the same range 1–77434. Continuity: **pass**. All legacy identifiers remain exact aliases.

## Dense positions

| riwāyah | words | empty slots | position range | contiguous |
|---|---:|---:|---|---|
| `hafs` | 77,432 | 2 | 1–77432 | yes |
| `shuba` | 77,432 | 2 | 1–77432 | yes |
| `bazzi` | 77,432 | 2 | 1–77432 | yes |
| `qaloun` | 77,431 | 3 | 1–77431 | yes |
| `warsh` | 77,431 | 3 | 1–77431 | yes |
| `douri` | 77,431 | 3 | 1–77431 | yes |
| `sousi` | 77,431 | 3 | 1–77431 | yes |

## Presence and absence: atomic slots

These remain word-sized slots. A riwāyah that lacks the word has no token at that slot, while its next token still receives the next dense position.

| slot | key | present | missing | forms with dense positions |
|---:|---|---|---|---|
| 25685 | `9:من#50` | bazzi | hafs, shuba, warsh, qaloun, douri, sousi | **مِن** `bazzi:p25685` |
| 60523 | `40:ان#5` | hafs, shuba | warsh, qaloun, douri, sousi, bazzi | **أَن** `hafs:p60522` · **أَن** `shuba:p60522` |
| 69720 | `57:هو#5` | hafs, shuba, douri, sousi, bazzi | warsh, qaloun | **هُوَ** `hafs:p69719` · **هُوَ** `shuba:p69719` · **هُوَ** `douri:p69718` · **هُّوَ** `sousi:p69718` · **هُوَ** `bazzi:p69719` |
| 73951 | `72:لو#1` | warsh, qaloun, douri, sousi | hafs, shuba, bazzi | **لَّوِ** `warsh:p73948` · **لَّوِ** `qaloun:p73948` · **لَّوِ** `douri:p73949` · **لَّوِ** `sousi:p73949` |
| 74227 | `73:لن#1` | hafs, shuba, warsh, qaloun, bazzi | douri, sousi | **لَّن** `hafs:p74225` · **لَّن** `shuba:p74225` · **لَّن** `warsh:p74224` · **لَّن** `qaloun:p74224` · **لَّن** `bazzi:p74225` |

### Bazzī’s `مِن` at 9:101

Shared slot **25685** contains **مِن** for Bazzī at dense position **p25685**. Bazzī’s local sequence is p25684, p25685, p25686; Ḥafṣ has no token in the middle slot, so its neighboring tokens remain consecutive at p25684 and p25685.

## Genuine n:m alignment spans

A span says that the whole token sequence corresponds; it does not claim that the first word on one side independently equals the first on the other.

### 40:60522-60523 — slots 60522–60523 (40:26 — `أَوْ أَن` / `وَأَن`)

| riwāyah | token sequence |
|---|---|
| `hafs` | أَوۡ أَن |
| `shuba` | أَوۡ أَن |
| `bazzi` | وَأَن |
| `qaloun` | وَأَنْ |
| `warsh` | وَأَنْ |
| `douri` | وَأَن |
| `sousi` | وَأَن |

### 72:73950-73951 — slots 73950–73951

| riwāyah | token sequence |
|---|---|
| `hafs` | وَأَلَّوِ |
| `shuba` | وَأَلَّوِ |
| `bazzi` | وَأَلَّوِ |
| `qaloun` | وَأَن لَّوِ |
| `warsh` | وَأَن لَّوِ |
| `douri` | وَأَن لَّوِ |
| `sousi` | وَأَن لَّوِ |

### 73:74226-74227 — slots 74226–74227

| riwāyah | token sequence |
|---|---|
| `hafs` | أَن لَّن |
| `shuba` | أَن لَّن |
| `bazzi` | أَن لَّن |
| `qaloun` | أَن لَّن |
| `warsh` | أَن لَّن |
| `douri` | أَلَّن |
| `sousi` | أَلَّن |

## Compatibility

Comparison schema 2.1 keeps `id` and adds `slot_id` plus a per-riwāyah `position` map. Muṣḥaf format 1.1 keeps `w`, adds its equal alias `s`, and adds dense `p`. Removing the legacy aliases requires a future major version.
