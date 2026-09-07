<?php

declare(strict_types=1);

namespace QuranText;

final class Surah extends Span
{
    public readonly string $nameAr;
    public readonly string $nameEn;
    public readonly string $revelation;
    public readonly bool $hasBasmalah;
    public readonly int $ayahCount;
    /** @internal index into ayah_starts of āyah 1 */
    public readonly int $firstAyah;

    public function __construct(Mushaf $mushaf, public readonly int $number)
    {
        if ($number < 1 || $number > 114) {
            throw new \OutOfRangeException("sūrah $number: there are 114");
        }
        $info = $mushaf->doc['surahs'][$number - 1];
        $starts = $mushaf->doc['surah_starts'];
        parent::__construct($mushaf, $starts[$number - 1], $starts[$number] ?? count($mushaf->words));
        $this->nameAr = $info['name_ar'];
        $this->nameEn = $info['name_en'];
        $this->revelation = $info['revelation'];
        $this->hasBasmalah = $info['has_basmalah'];
        $this->ayahCount = $info['ayah_count'];
        $this->firstAyah = $info['first_ayah'];
    }

    /** @return Ayah[] */
    public function ayahs(): array
    {
        $out = [];
        for ($n = 1; $n <= $this->ayahCount; $n++) {
            $out[] = new Ayah($this->mushaf, $this->number, $n);
        }
        return $out;
    }

    public function ayah(int $number): Ayah
    {
        return new Ayah($this->mushaf, $this->number, $number);
    }

    /**
     * The basmalah where it is printed unnumbered before āyah 1 (Warsh,
     * Qālūn, Dūrī, Sūsī at al-Fātiḥah); null otherwise.
     */
    public function basmalah(): ?Span
    {
        $first = $this->mushaf->doc['ayah_starts'][$this->firstAyah];
        return $first > $this->start ? new Span($this->mushaf, $this->start, $first) : null;
    }

    public function firstPage(): Page
    {
        return $this->page();
    }

    public function lastPage(): Page
    {
        return $this->mushaf->pageAt($this->end - 1);
    }
}
