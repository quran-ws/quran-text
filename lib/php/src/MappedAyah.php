<?php

declare(strict_types=1);

namespace QuranText;

/**
 * Where a Kūfī āyah falls in one edition.  $relation is same, merged, split
 * (then $ayahLast is set), shifted or unnumbered ($ayah is 0).
 */
final class MappedAyah
{
    public function __construct(
        public readonly int $surah,
        public readonly int $ayah,
        public readonly string $relation,
        public readonly ?int $ayahLast = null,
    ) {
    }

    /** "2:253-254" */
    public function key(): string
    {
        return $this->ayahLast ? "{$this->surah}:{$this->ayah}-{$this->ayahLast}" : "{$this->surah}:{$this->ayah}";
    }

    public function __toString(): string
    {
        return $this->key();
    }
}
