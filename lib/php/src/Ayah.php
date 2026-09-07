<?php

declare(strict_types=1);

namespace QuranText;

/** One numbered āyah, in this edition's own count. */
final class Ayah extends Span
{
    public readonly Surah $surah;
    /** 0-based ordinal of the āyah in the muṣḥaf. */
    public readonly int $index;

    public function __construct(Mushaf $mushaf, int $surah, public readonly int $number)
    {
        $s = $mushaf->surah($surah);
        if ($number < 1 || $number > $s->ayahCount) {
            throw new \OutOfRangeException("{$s->nameEn} has {$s->ayahCount} āyāt in {$mushaf->nameEn}, not $number");
        }
        $k = $s->firstAyah + $number - 1;
        $starts = $mushaf->doc['ayah_starts'];
        parent::__construct($mushaf, $starts[$k], $starts[$k + 1] ?? count($mushaf->words));
        $this->surah = $s;
        $this->index = $k;
    }

    /** @internal */
    public static function fromIndex(Mushaf $mushaf, int $k): self
    {
        $s = $mushaf->surahs[$mushaf->surahOfAyahIndex($k)];
        return new self($mushaf, $s->number, $k - $s->firstAyah + 1);
    }

    /** "2:255" */
    public function key(): string
    {
        return "{$this->surah->number}:{$this->number}";
    }

    /** The printed line the āyah starts on. */
    public function line(): ?Line
    {
        return $this->mushaf->lineAt($this->start);
    }

    /** Every printed line the āyah touches. @return Line[] */
    public function lines(): array
    {
        return $this->mushaf->linesBetween($this->start, $this->end);
    }

    /** @return array<int, ?string>|null */
    public function rasm_imlai(): ?array
    {
        $col = $this->mushaf->doc['rasm_imlai'];
        return $col ? array_slice($col, $this->start, $this->end - $this->start) : null;
    }

    public function hasSajdah(): bool
    {
        foreach ($this->marks() as ['mark' => $mark]) {
            if ($mark->kind === 'sajdah') {
                return true;
            }
        }
        return false;
    }

    /** ۝٢٥٥ */
    public function marker(): string
    {
        return Text::ayahMark($this->number);
    }

    /** The shared numbers of this āyah's words. @return array<int,true> */
    public function numbers(): array
    {
        $runs = $this->mushaf->numbers();
        $missing = $this->mushaf->missingNumbers();
        $out = [];
        for ($n = $runs[$this->start][0], $last = $runs[$this->end - 1][1]; $n <= $last; $n++) {
            if (!isset($missing[$n])) {
                $out[$n] = true;
            }
        }
        return $out;
    }

    /**
     * This āyah in another riwāyah: $hafs->ayah(2, 255)->to($warsh) → 2:253-254, split.
     * Computed from the shared numbering, so it works between any two riwāyāt.
     */
    public function to(Mushaf $other): AyahMatch
    {
        $mine = $this->numbers();
        $hits = [];
        $unnumbered = false;
        foreach (array_keys($mine) as $n) {
            $w = $other->wordByNumber($n);
            if ($w === null) {
                continue;
            }
            $a = $w->ayah();
            if ($a === null) {
                $unnumbered = true;
            } elseif (!$hits || end($hits)->index !== $a->index) {
                $hits[] = $a;
            }
        }
        if (!$hits) {
            return new AyahMatch([], $unnumbered ? 'unnumbered' : 'missing');
        }
        if (count($hits) > 1) {
            return new AyahMatch($hits, 'split');
        }
        $theirs = $hits[0]->numbers();
        $superset = !array_diff_key($mine, $theirs);
        $same = $superset && count($theirs) === count($mine);
        return new AyahMatch($hits, $same ? 'same' : ($superset ? 'merged' : 'shifted'));
    }

    public function next(): ?self
    {
        $k = $this->index + 1;
        return $k < $this->mushaf->ayahCount() ? self::fromIndex($this->mushaf, $k) : null;
    }

    public function previous(): ?self
    {
        $k = $this->index - 1;
        return $k >= 0 ? self::fromIndex($this->mushaf, $k) : null;
    }

    public function __toString(): string
    {
        return $this->key();
    }
}
