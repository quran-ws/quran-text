<?php

declare(strict_types=1);

namespace QuranText;

/** One printed word and everything the muṣḥaf says about it. */
final class Word
{
    public function __construct(private readonly Mushaf $mushaf, public readonly int $position)
    {
        if ($position < 0 || $position >= count($mushaf->words)) {
            throw new \OutOfRangeException("position $position is outside the muṣḥaf");
        }
    }

    public function text(): string
    {
        return $this->mushaf->words[$this->position];
    }

    /** Plain modern spelling, Ḥafṣ only; null elsewhere. */
    public function imlaei(): ?string
    {
        $col = $this->mushaf->doc['imlaei'];
        return $col ? $col[$this->position] : null;
    }

    public function sura(): Sura
    {
        return $this->mushaf->suraAt($this->position);
    }

    /** The āyah this word is in; null for the unnumbered basmalah. */
    public function ayah(): ?Ayah
    {
        return $this->mushaf->ayahAt($this->position);
    }

    /** 1-based position within the āyah; null when unnumbered. */
    public function index(): ?int
    {
        $a = $this->ayah();
        return $a === null ? null : $this->position - $a->start + 1;
    }

    public function page(): Page
    {
        return $this->mushaf->pageAt($this->position);
    }

    public function line(): ?Line
    {
        return $this->mushaf->lineAt($this->position);
    }

    public function juz(): ?Juz
    {
        return $this->mushaf->juzAt($this->position);
    }

    /** The shared number: the same word in every riwāyah. */
    public function number(): int
    {
        return $this->mushaf->numbers()[0][$this->position];
    }

    /** Equal to number() except where this muṣḥaf writes two numbers as one word. */
    public function numberLast(): int
    {
        return $this->mushaf->numbers()[1][$this->position];
    }

    /** @return Mark[] */
    public function marks(): array
    {
        return $this->mushaf->marksAt[$this->position] ?? [];
    }

    public function hasMark(string $kind): bool
    {
        foreach ($this->marks() as $mark) {
            if ($mark->kind === $kind) {
                return true;
            }
        }
        return false;
    }

    /** The same word in another riwāyah, by the shared number; null where it does not read it. */
    public function to(Mushaf $other): ?Word
    {
        return $other->wordByNumber($this->number());
    }

    /** The word with its signs: ۞ before, waqf and ۩ after. */
    public function render(bool|array $marks = true): string
    {
        $kinds = Text::markKinds($marks);
        $before = '';
        $after = '';
        foreach ($this->marks() as $mark) {
            if (!isset($kinds[$mark->kind])) {
                continue;
            }
            if ($mark->side === 'before') {
                $before .= $mark->sign . ' ';
            } else {
                $after .= $mark->sign;
            }
        }
        return $before . $this->text() . $after;
    }

    public function __toString(): string
    {
        return $this->text();
    }
}
