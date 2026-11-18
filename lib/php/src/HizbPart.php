<?php

declare(strict_types=1);

namespace QuranText;

/** A part of a ḥizb: a rubu_al_hizb or a thumn. */
abstract class HizbPart extends Division
{
    /** The ḥizb this part sits in. */
    public function hizb(): Hizb
    {
        return $this->mushaf->hizbAt($this->start);
    }

    /** 1-based place inside its ḥizb: 1–4 for a rubu_al_hizb, 1–8 for a thumn. */
    public function numberInHizb(): int
    {
        $per = intdiv(count($this->mushaf->doc[static::LAYER . '_starts']), 60);
        return ($this->number - 1) % $per + 1;
    }
}
