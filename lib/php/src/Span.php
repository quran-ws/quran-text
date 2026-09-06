<?php

declare(strict_types=1);

namespace QuranText;

/** A run of positions start … end-1 of one muṣḥaf. */
class Span implements \Countable, \IteratorAggregate
{
    public function __construct(
        protected readonly Mushaf $mushaf,
        public readonly int $start,
        public readonly int $end,
    ) {
    }

    public function mushaf(): Mushaf
    {
        return $this->mushaf;
    }

    public function count(): int
    {
        return $this->end - $this->start;
    }

    /** @return string[] */
    public function words(): array
    {
        return array_slice($this->mushaf->words, $this->start, $this->end - $this->start);
    }

    /** @return Word[] */
    public function wordList(): array
    {
        $out = [];
        for ($p = $this->start; $p < $this->end; $p++) {
            $out[] = new Word($this->mushaf, $p);
        }
        return $out;
    }

    public function getIterator(): \Iterator
    {
        return new \ArrayIterator($this->wordList());
    }

    /** The words joined with spaces, without any sign. */
    public function text(): string
    {
        return implode(' ', $this->words());
    }

    /**
     * The text as the muṣḥaf prints it, with what you ask for.
     *
     * $marks: true for every sign, or an array of kinds among "waqf", "hizb",
     * "sajdah".  $ayahMarkers appends ۝ with the āyah number after each āyah
     * that ends inside the span.  $lines breaks the text where the printed
     * lines break.
     */
    public function render(bool|array $marks = false, bool $ayahMarkers = false, bool $lines = false): string
    {
        $m = $this->mushaf;
        $kinds = Text::markKinds($marks);
        $lineStarts = $lines ? $m->lineStartSet : null;
        $out = '';
        for ($pos = $this->start; $pos < $this->end; $pos++) {
            if ($lineStarts !== null && $pos !== $this->start && isset($lineStarts[$pos])) {
                $out .= "\n";
            } elseif ($pos !== $this->start) {
                $out .= ' ';
            }
            $token = $m->words[$pos];
            foreach ($m->marksAt[$pos] ?? [] as $mark) {
                if (!isset($kinds[$mark->kind])) {
                    continue;
                }
                $token = $mark->side === 'before' ? $mark->sign . ' ' . $token : $token . $mark->sign;
            }
            $out .= $token;
            if ($ayahMarkers && isset($m->ayahEnds[$pos])) {
                $out .= ' ' . Text::ayahMarker($m->ayahNumber($m->ayahEnds[$pos]));
            }
        }
        return $out;
    }

    /** Every numbered āyah with at least one word in the span. @return Ayah[] */
    public function ayat(): array
    {
        $starts = $this->mushaf->doc['ayah_starts'];
        $first = max(Text::indexOf($starts, $this->start), 0);
        $last = Text::indexOf($starts, $this->end - 1);
        $out = [];
        for ($k = $first; $k <= $last; $k++) {
            $out[] = Ayah::fromIndex($this->mushaf, $k);
        }
        return $out;
    }

    public function firstAyah(): ?Ayah
    {
        $a = $this->ayat();
        return $a[0] ?? null;
    }

    public function lastAyah(): ?Ayah
    {
        $a = $this->ayat();
        return $a ? $a[count($a) - 1] : null;
    }

    /** @return Sura[] */
    public function suras(): array
    {
        $starts = $this->mushaf->doc['sura_starts'];
        $first = Text::indexOf($starts, $this->start);
        $last = Text::indexOf($starts, $this->end - 1);
        return array_slice($this->mushaf->suras, $first, $last - $first + 1);
    }

    /** @return Page[] */
    public function pages(): array
    {
        $starts = $this->mushaf->doc['page_starts'];
        $first = Text::indexOf($starts, $this->start);
        $last = Text::indexOf($starts, $this->end - 1);
        $out = [];
        for ($n = $first; $n <= $last; $n++) {
            $out[] = new Page($this->mushaf, $n + 1);
        }
        return $out;
    }

    /** The page the span starts on. */
    public function page(): Page
    {
        return $this->mushaf->pageAt($this->start);
    }

    public function juz(): ?Juz
    {
        return $this->mushaf->juzAt($this->start);
    }

    /** Every sign inside the span, with the word it is printed on. @return array<int, array{word: Word, mark: Mark}> */
    public function marks(): array
    {
        $out = [];
        for ($p = $this->start; $p < $this->end; $p++) {
            foreach ($this->mushaf->marksAt[$p] ?? [] as $mark) {
                $out[] = ['word' => new Word($this->mushaf, $p), 'mark' => $mark];
            }
        }
        return $out;
    }

    /** The $index-th word of the span, 1-based. */
    public function word(int $index): Word
    {
        if ($index < 1 || $index > $this->count()) {
            throw new \OutOfRangeException("word $index: the span has {$this->count()} words");
        }
        return new Word($this->mushaf, $this->start + $index - 1);
    }
}
