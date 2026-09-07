<?php

declare(strict_types=1);

namespace QuranText;

/**
 * Where an āyah falls in another riwāyah.  $relation: same (one āyah, the
 * same words), merged (one āyah holding more), split (several āyāt), shifted
 * (one āyah, boundaries crossing), unnumbered (the basmalah printed without a
 * number), missing (no word of it).
 */
final class AyahMatch
{
    /** @param Ayah[] $ayat */
    public function __construct(public readonly array $ayat, public readonly string $relation)
    {
    }

    public function first(): ?Ayah
    {
        return $this->ayat[0] ?? null;
    }

    public function last(): ?Ayah
    {
        return $this->ayat ? $this->ayat[count($this->ayat) - 1] : null;
    }

    /** "2:253-254" */
    public function key(): string
    {
        if (!$this->ayat) {
            return '';
        }
        $a = $this->first();
        $b = $this->last();
        return $a->index === $b->index ? $a->key() : $a->key() . '-' . $b->number;
    }

    public function __toString(): string
    {
        return ($this->key() ?: '-') . " ({$this->relation})";
    }
}
